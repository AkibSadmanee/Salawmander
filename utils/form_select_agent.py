from pydantic import BaseModel, Field
from typing import List
from pydantic_ai import Agent
import json

with open("config.json", "r") as f:
    config = json.load(f)

class Form(BaseModel):
    form_name: str = Field(..., description="Unchanged full name of the Form.")
    justification: str = Field(..., description="One line Justification for the form selection directed to the user.")

class FormResponse(BaseModel):
    forms: List[Form] = Field(..., description="List of forms with their names and justifications.")

form_select_agent = Agent(
    config["form_select_agent_model"],
    deps_type=None,
    output_type=FormResponse,
    system_prompt="""A user query can mention one or more forms from the following list. Process the user query to decide which form(s) from the following list they are asking about. 
Return a list of Form(s) you find relevant. Each Form will have a `form_name` picked from the given list and a *one-line* `justification` directed to the user explaining why you selected that form.
If you can't find any match, return a list of Forms where the `form_name` is a empty string and a suitable *one-line* justification directed to the user.
Remember that the users can make simple typos.

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
"""
)