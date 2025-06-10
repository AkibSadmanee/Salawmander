from flask import Flask, render_template, request, redirect, url_for
import openai
import urllib.parse
import json
from pydantic import BaseModel, Field
from typing import List
from pydantic_ai import Agent

from utils.form_select_agent import form_select_agent


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":
        data = request.get_json()
        user_query = data.get("query", "")
        response = await form_select_agent.run(user_query)
        forms_found = [form.model_dump() for form in response.output.forms]
        return {"forms": forms_found, "query": user_query}
    return render_template("index.html")

@app.route("/form")
def form():
    info = request.args.get("info", "")
    return render_template("formPage.html", processed_info=info)



if __name__ == "__main__":
    app.run(debug=True)