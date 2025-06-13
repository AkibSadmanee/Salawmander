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
    "gpt-4.1",
    deps_type=None,
    output_type=FormResponse,
    system_prompt="""Given a user query, identify which legal form(s) from the list below the user is requesting or referring to. The query may contain typos or informal language, and **may mention one or more forms**.
Consider misspellings, synonyms, and vague references. Carefully analyze the query so that you don't miss any form(s).

*List of available forms:*
- Certificate of Service
- Counterclaim
- Non Hearing Motion for Continuance
- Notice of Dismissal
- Order Continuing Small Claims Case
- Request for Relief from Court Costs
- Small Claims - Statement of Claim - General
- Small Claims - Statement of Claim - Security Deposit
- Stipulation for Dismissal
"""
)