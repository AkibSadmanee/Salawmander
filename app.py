from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from pydantic_ai import Agent
from datetime import datetime

from utils.form_select_agent import form_select_agent
from utils.forms import user_forms
from utils.helpers import get_percentage, generate_html_form



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


selected_forms: List[dict] = []
initial_message = "Hi!! Could you provide some basic information about you to start filling the forms? Something like your name, address, etc."
chat_messages = []

class UpdateValueStructure(BaseModel):
    key: str = Field(..., description="The name of the field to update.")
    value: Any = Field(..., description="The value to set for the field.")

class Response(BaseModel):
    response: str = Field(None, description="A question for the user if more information is needed, a completion note otherwise.")
    

fill_json_agent = Agent(
    "gpt-4.1",
    deps_type=None,
    output_type=Response,
    system_prompt="""You are an AI assistant that helps users fill out all the forms at the same time by asking relevant questions in simple terms.
You will load the current list of forms (python dictionaries) using the get_most_recent_forms tool.
You will analyze the user message and update the all the fields of the relevant forms that you can confidently fill with the provided information by passing a python dictionary (where the keys are the field names and the values are the user-provided values) to the update_json tool.
The update_json tool will iterate over all the loaded forms and update the values for all the fields in all the forms where the keys match with the dictionary you provide.

*Important rules:*
If there are missing values in the updated JSON object, ask for one to the user. Make sure to explain in very simple terms what the user should answer your query with.
You never ask for a value that is already filled in the JSON object unless a contradiction occurs.
If all the fields of the json object are filled, return a completion note instead of a query.
If you can't fill any field of the JSON object, return a question to the user asking for a missing value from the loaded JSON.
Only enter human names in the defendant and plaintiff fields.
You may call each tool only once per run.
If the user provides information that conflicts with already-filled fields, ask for clarification before updating.
Be very careful about what values you fill in what keys of the JSON object. If you are not sure about the value, ask the user to clarify.
The Division can only be one of the following: "Honolulu", "Ewa", "Ko'olauloa", "Ko'olaupoko", "Wai'anae", "Waialua", "Wahiawa".
The Circuit can only be one of the following: "First: Oahu", "Second:Maui, Moloka'i Lāna'i", "Third: Hawaii (AKA Big Island)", "Fifth: Kauai'i".
Always convert dates to the format MM/DD/YYYY even if the user says something like 10th of June 2018. In case you need today's date, use the get_today_date tool.
"""
)

@fill_json_agent.tool_plain
def get_most_recent_forms() -> list[dict]:
    return selected_forms


@fill_json_agent.tool_plain
def update_json(**updates):
    for key, value in updates.items():
        for d in selected_forms:
            if key in d:
                d[key] = value


@fill_json_agent.tool_plain
def get_today_date():
    return datetime.today().strftime("%m/%d/%Y")


@app.get("/")
async def root(request: Request):
    global selected_forms, initial_message, chat_messages

    selected_forms = []
    initial_message = "Hi!! Could you provide some basic information about you to start filling the forms? Something like your name, address, etc."
    chat_messages = []
    
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def post_root(request: Request):
    global initial_message
    data = await request.json()
    user_query = data.get("query", "")
    print("Here 1")
    response = await form_select_agent.run(user_query)
    print("Here 2")
    
    forms_found = [form.model_dump() for form in response.output.forms]
    
    print(f"Forms found: {forms_found}")

    for form in forms_found:
        if form["form_name"]:
            selected_forms.append(user_forms[form["form_name"]]().model_dump())
            selected_forms[-1]["form_name"] = form["form_name"]

    print(f"Selected forms 1: {selected_forms}")
    print("Here 3")
    fill_response = await fill_json_agent.run(user_query)
    print("Here 4")
    initial_message = fill_response.output.response
    chat_messages.append({"role": "salawmander", "content": initial_message})
    print(f"Selected forms x: {selected_forms}")
    return JSONResponse(content={"forms": forms_found})


@app.get("/form")
async def form(request: Request, info: str = ""):
    form_progress_data = [
        {
            "form_name": form.get("form_name", f"Form {i + 1}"),
            "progress": get_percentage(form)
        }
        for i, form in enumerate(selected_forms)
    ]
    
    return templates.TemplateResponse(
        "formPage.html",
        {
            "request": request,
            "processed_info": info,
            "chat_history": chat_messages,
            "forms": form_progress_data
        }
    )


@app.post("/form-fill")
async def form_fill(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    chat_messages.append({"role": "user", "content": user_query})


    query = ""
    if len(chat_messages) < 4:
        for chat in chat_messages:
            query += f"{chat['role'].capitalize()}: {chat['content']}\n"
    else:
        for i, chat in enumerate(chat_messages):
            if i >= len(chat_messages) - 4:
                query += f"{chat['role'].capitalize()}: {chat['content']}\n"

    response = await fill_json_agent.run(query)

    result_message = response.output.response
    chat_messages.append({"role": "salawmander", "content": result_message})

    return JSONResponse(content={
        "message": result_message,
        "forms": [
            {
                "form_name": form.get("form_name", f"Form {i+1}"),
                "progress": get_percentage(form)
            }
            for i, form in enumerate(selected_forms)
        ]
    })


@app.post("/get_html")
async def get_html(request: Request):
    data = await request.json()
    form_name = data.get("form_name")
    print(f"Selected forms 2: {selected_forms}")
    print()
    print(f"Received form_name: {form_name}")
    # Validate form_name
    if not form_name:
        raise HTTPException(status_code=400, detail="form_name is required.")

    # Search for matching form
    matched_form = next((f for f in selected_forms if f.get("form_name") == form_name), None)
    print(f"Matched form: {matched_form}")
    if not matched_form:
        raise HTTPException(status_code=404, detail="Form not found.")

    html_content = generate_html_form(matched_form)
    return HTMLResponse(content=html_content) 



@app.post("/save_html")
async def save_html(request: Request):
    form_data = await request.form()
    form_dict = dict(form_data)

    for i, form in enumerate(selected_forms):
        if form.get("form_name") == form_dict.get("form_name"):
            selected_forms[i].update(form_dict)
            break
    
    fill_response = await fill_json_agent.run(
        f"User updated the form {form_dict.get('form_name')}. Please acknowledge the update and proceed farther."
    )
    chat_messages.append({"role": "salawmander", "content": fill_response.output.response})
    
    return JSONResponse(content={"message": fill_response.output.response}, status_code=200)