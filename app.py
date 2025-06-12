from flask import Flask, render_template, request, redirect, url_for, jsonify

from pydantic import BaseModel, Field

from pydantic import BaseModel, Field
from typing import Dict, Any
from pydantic_ai import Agent

from utils.form_select_agent import form_select_agent
from utils.forms import user_forms

app = Flask(__name__)

selected_forms = []
initial_message = "Hi!! Could you provide some basic information about you to start filling the forms? Something like your name, address, etc."
chat_messages = []

class UpdateJsonInput(BaseModel):
    new_data: Dict[str, Any] = Field(..., description="Dictionary where keys are field names and values are the user-provided values.")


class Response(BaseModel):
    response: str = Field(None, description="A question for the user if more information is needed, a completion note otherwise.")
    
def get_percentage(JSON):
    """Calculate the percentage of fields filled in the selected forms."""
    counter = 0
    keys = list(JSON.keys())
    values = list(JSON.values())
    for key, values in JSON.items():
        if key == "form_name":
            continue
        elif values != None:
            counter += 1
    try:
        decimal = counter/len(keys) if keys else 0
    except ZeroDivisionError:
        decimal = 0
    percentage = round(decimal * 100, 0)
    return percentage



fill_json_agent = Agent(
    "gpt-4.1",
    deps_type=None,
    output_type=Response,
    system_prompt="""You are an AI assistant that helps users fill out forms. Remember that the users can make simple typos.
You will load the most recent JSON data using the `get_most_recent_json` tool.
You will process the user message and update the all the fields of the JSON object that you can fill with the provided information using the `update_json` tool. Pass a dictionary where the keys are the field names and the values are the user-provided values.
You will always return a response. 
*Important rules:*
If there are missing values in the updated JSON object, ask for one to the user. Make sure to explain in very simple terms what the user should answer your query with.
If all the fields of the json object are filled, return a completion note.
If you can't fill any field of the JSON object, return a question to the user asking for a missing value from the JSON.
If you are not sure about whether the user is a defendant or a plaintiff, ask the user to clarify their role in the case.
You may call each tool only once per run.
Completely ignore the fields of the JSON object that are not empty or None.
The Division can only be one of the following: "Honolulu", "Ewa", "Ko'olauloa", "Ko'olaupoko", "Wai'anae", "Waialua", "Wahiawa".
The Circuit can only be one of the following: "First: Oahu", "Second:Maui, Moloka'i Lāna'i", "Third: Hawaii (AKA Big Island)", "Fifth: Kauai'i".
"""
)

@fill_json_agent.tool_plain  
def get_most_recent_json() -> dict:
    """Get the most recent JSON data from the form."""
    return selected_forms


@fill_json_agent.tool_plain
def update_json(**updates):
    """Update the selected forms with the provided dictionary."""
    for key, value in updates.items():
        for d in selected_forms:
            if key in d:
                d[key] = value


@app.route("/", methods=["GET", "POST"])
async def index():
    global initial_message
    if request.method == "POST":
        data = request.get_json()
        user_query = data.get("query", "")
        response = await form_select_agent.run(user_query)
        forms_found = [form.model_dump() for form in response.output.forms]
        for form in forms_found:
            if form["form_name"]:
                selected_forms.append(user_forms[form["form_name"]]().model_dump())
                selected_forms[-1]["form_name"] = form["form_name"]

        response = await fill_json_agent.run(user_query)
        initial_message = response.output.response
        chat_messages.append({"role": "salawmander", "content": initial_message})
        return {"forms": forms_found}
    return render_template("index.html")


@app.route("/form")
def form():
    info = request.args.get("info", "")
    form_progress_data = [
        {
            "form_name": form.get("form_name", f"Form {i+1}"),
            "progress": get_percentage(form)
        }
        for i, form in enumerate(selected_forms)
    ]
    return render_template(
        "formPage.html",
        processed_info=info,
        chat_history=chat_messages,
        forms=form_progress_data
    )


@app.route("/form-fill", methods=["POST"])
async def form_fill():
    data = request.get_json()
    user_query = data.get("query", "")
    chat_messages.append({"role": "user", "content": user_query})
    query = chat_messages[-1]["content"]+ "\n\nuser query: " + user_query
    response = await fill_json_agent.run(query)
    result_message = response.output.response
    chat_messages.append({"role": "salawmander", "content": result_message})

    return jsonify({
        "message": result_message,
        "forms": [
            {
                "form_name": form.get("form_name", f"Form {i+1}"),
                "progress": get_percentage(form)
            }
            for i, form in enumerate(selected_forms)
        ]
    })


# @app.route("/get_html", methods=["POST"])
# def get_html():
#     pass



if __name__ == "__main__":
    app.run(debug=True)