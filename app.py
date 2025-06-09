from flask import Flask, render_template, request, redirect, url_for
import openai
import urllib.parse
import json

app = Flask(__name__)
with open("config.json", "r") as f:
    config = json.load(f)

client = openai.OpenAI(api_key=config["openai_api_key"])


def get_openai_response(query):
    system_prompt = """Process the user query to decide which forms from the following list the user asks about. 
Return ONLY a Python list as your output. Each element must be a dictionary with "form_name" and "justification". 
If you can't find any match, return a list with a single dictionary: {"form_name": "", "justification": "<polite explanation for the user>"}.
The form names should be exactly as they appear in the provided list.

List of available forms:
Certificate of Service
Counterclaim
Non Hearing Motion for Continuance
Notice of Dismissal
Order Continuing Small Claims Case
Request for Relief from Court Costs
Small Claims - Statement of Claim - General
Small Claims - Statement of Claim - Security Deposit
Stipulation for Dismissal

Return: 
[
{"form_name": str, "justification": str}, 
...
]
"""
    ai_response = client.chat.completions.create(
        model=config["model"],
        temperature=0.0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    response =  eval(ai_response.choices[0].message.content)
    try:
        assert isinstance(response, list) and len(response) > 0 and "form_name" in response[0] and "justification" in response[0]
    except AssertionError as e:
        response = [{"form_name": "", "justification": "Sorry, I couldn't process your request for an internal error. Please try again."}]
    
    return response



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        user_query = data.get("query", "")
        forms_found = get_openai_response(user_query)
        return {"forms": forms_found, "query": user_query}
    return render_template("index.html")

@app.route("/form")
def form():
    info = request.args.get("info", "")
    return render_template("formPage.html", processed_info=info)



if __name__ == "__main__":
    app.run(debug=True)