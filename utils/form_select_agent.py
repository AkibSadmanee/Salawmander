from pydantic import BaseModel, Field
from typing import List
from pydantic_ai import Agent
import json

with open("config.json", "r") as f:
    config = json.load(f)

class Form(BaseModel):
    form_name: str = Field(..., description="Unchanged full name of a single Form.")
    justification: str = Field(..., description="One line Justification mentioning which part of the query made you select this form.")

class FormResponse(BaseModel):
    forms: List[Form] = Field(..., description="List of forms with their names and justifications.")

form_select_agent = Agent(
    "gpt-4.1",
    deps_type=None,
    output_type=FormResponse,
    system_prompt="""Given a user query, identify which legal form(s) the user is referring to from the list of available forms below. The query may contain typos or informal language, and may mention more than one forms.
Consider misspellings, synonyms, and vague references. 
Carefully analyze the query so that you don't miss any form(s). The user may ask for multiple forms in one query, and you should return all relevant forms as a list of Forms. The query may contain any combination of the forms listed below, and you should identify all that apply and return a list of Form(s).

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


For example, the user may ask for "Counterclaim and Certificate of Service" or "I need a form for a non-hearing motion for continuance and a form to agree to settle on a case". You should identify the "Counterclaim" and "Certificate of Service" or the "Non Hearing Motion for Continuance", and "Stipulation for Dismissal" form pairs.

"""
)