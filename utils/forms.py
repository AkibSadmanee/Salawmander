from typing import List, Optional
from pydantic import BaseModel, Field

class Recipient(BaseModel):
    # Write the full name of the person who was served
    name: str = Field(..., description="Full name of the person served.")
    # Write the mailing address of the person who was served
    address: str = Field(..., description="Mailing address of the person served.")

class CertificateOfService(BaseModel):
    # Name of the court location (e.g., 'Honolulu', 'Kauai')
    division: Optional[str] = Field(None, description="Name of the court location (e.g., 'Honolulu', 'Kauai').")
    # Case number (found on other court papers)
    civil_number: Optional[str] = Field(None, description="Case number, found on court papers.")
    # Full name(s) of the person/people who started the case
    plaintiffs: Optional[str] = Field(None, description="Full name(s) of the plaintiff(s).")
    # Full name(s) of the person/people being sued
    defendants: Optional[str] = Field(None, description="Full name(s) of the defendant(s).")
    # Your name and contact info, or your lawyer's name and contact info
    filing_party_or_attorney: Optional[str] = Field(
        None, 
        description="Name and contact info of the filing party or their attorney."
    )
    # Name of the document served, and the date filed with the court
    documents_served: Optional[str] = Field(
        None, 
        description="Name of the document served and date filed with court."
    )
    # Date you served the document
    service_date: Optional[str] = Field(
        None, 
        description="Exact date the document was served or mailed."
    )
    # How you served the document: 'Hand-delivery' or 'Mail'
    service_method: Optional[str] = Field(
        None, 
        description="Method of service: 'Hand-delivery' or 'Mail'."
    )
    # List of recipients (each with name and address)
    recipient_names_and_addresses: List[Recipient] = Field(
        default_factory=list, 
        description="List of recipients with names and mailing addresses."
    )
    # Print or type your full name
    typed_name: Optional[str] = Field(None, description="Your typed or printed name.")
    # Date you signed the form
    date_signed: Optional[str] = Field(None, description="Date of signature.")



class Counterclaim(BaseModel):
    # Name of the court location (e.g., 'Honolulu', 'Maui')
    division: Optional[str] = Field(
        None,
        description="Name of the court location (e.g., 'Honolulu', 'Maui')."
    )
    # Case number from court documents
    civil_number: Optional[str] = Field(
        None,
        description="Case number from your court documents."
    )
    # Full name of the person who first started the case (plaintiff)
    plaintiffs: Optional[str] = Field(
        None,
        description="Full name of the plaintiff (the person who started the case)."
    )
    # Your full name (the defendant)
    defendants: Optional[str] = Field(
        None,
        description="Your full name (the defendant making this counterclaim)."
    )
    # Your contact details, or your attorney's (name, law firm, contact info)
    defendant_or_attorney_info: Optional[str] = Field(
        None,
        description="Your name and contact info, or your attorney's."
    )
    # Date (or approx date) the plaintiff owed you money
    date_money_owed: Optional[str] = Field(
        None,
        description="Date or approximate date when the plaintiff owed you money."
    )
    # Explanation and breakdown of amount owed
    amount_breakdown: Optional[str] = Field(
        None,
        description="Explanation of why the plaintiff owes you money and how you calculated the total."
    )
    # Total amount requested from the court
    judgment_amount: Optional[str] = Field(
        None,
        description="Total amount you are asking the court to order the plaintiff to pay."
    )
    # Date Counterclaim was served on the plaintiff
    service_date: Optional[str] = Field(
        None,
        description="Date when you gave or mailed a copy of this Counterclaim to the plaintiff."
    )
    # Method of service: 'Hand-delivery' or 'Mail'
    service_method: Optional[str] = Field(
        None,
        description="How you served the Counterclaim: 'Hand-delivery' or 'Mail'."
    )
    # Mailing address where the Counterclaim was sent/given to plaintiff
    service_address: Optional[str] = Field(
        None,
        description="Mailing address where you sent or gave the Counterclaim to the plaintiff."
    )
    # Date you signed the certificate of service
    certificate_signature_date: Optional[str] = Field(
        None,
        description="Date when you signed the certificate confirming service."
    )
    # Printed/typed name below certificate signature
    certificate_name: Optional[str] = Field(
        None,
        description="Print or type your name below your certificate signature."
    )
    # Date you signed the declaration
    declaration_signature_date: Optional[str] = Field(
        None,
        description="Date when you signed the Declaration section."
    )
    # Printed/typed name below declaration signature
    declaration_name: Optional[str] = Field(
        None,
        description="Print or type your name below your declaration signature."
    )


class NonHearingMotionForContinuance(BaseModel):
    # Name of the court location (e.g., 'Honolulu', 'Kauai')
    division: Optional[str] = Field(
        None, description="Name of the court location (e.g., 'Honolulu', 'Kauai')."
    )
    # Case number
    civil_number: Optional[str] = Field(
        None, description="Case number, as found on your court papers."
    )
    # Full name of the plaintiff (person who started the case)
    plaintiffs: Optional[str] = Field(
        None, description="Full name of the plaintiff (the person who started the case)."
    )
    # Your full name (person requesting continuance)
    defendants: Optional[str] = Field(
        None, description="Your full name (the defendant requesting more time)."
    )
    # Name and contact details of person filing (or attorney)
    filing_party_info: Optional[str] = Field(
        None, description="Your name and contact info, or your lawyer's information."
    )
    # Type of hearing to be continued (e.g. 'Trial', 'Pre-Trial')
    type_of_motion: Optional[str] = Field(
        None, description="Type of hearing to delay (e.g., 'Trial', 'Pre-Trial')."
    )
    # Other type of hearing not listed above
    other_type: Optional[str] = Field(
        None, description="Other type of hearing (e.g., 'Mediation', 'Status Conference')."
    )
    # Reason for needing more time or to change the date
    reason_for_continuance: Optional[str] = Field(
        None, description="Reason for requesting continuance."
    )
    # The currently scheduled date and time
    old_date_time: Optional[str] = Field(
        None, description="Original date and time scheduled for hearing."
    )
    # The new date and time being requested
    new_date_time: Optional[str] = Field(
        None, description="New date and time requested."
    )
    # How many prior continuance requests have been made
    number_of_prior_continuances: Optional[str] = Field(
        None, description="Number of prior continuance requests."
    )
    # Name of opposing party or their attorney
    opposing_party_name: Optional[str] = Field(
        None, description="Name of the opposing party or their lawyer."
    )
    # Date this motion was served to the opposing party
    certificate_service_date: Optional[str] = Field(
        None, description="Date the motion was delivered or mailed to the other party."
    )
    # How motion was served: 'Hand-delivery' or 'Mail'
    service_method: Optional[str] = Field(
        None, description="Method of service: 'Hand-delivery' or 'Mail'."
    )
    # Address where the motion was delivered or mailed
    service_address: Optional[str] = Field(
        None, description="Address where the motion was delivered or mailed."
    )

    # Name of filing party (typed or printed)
    filing_party_name: Optional[str] = Field(
        None, description="Typed or printed name under signature."
    )
    # The other party's response: agree/disagree
    response_choice: Optional[str] = Field(
        None, description="Response from the other party (agree or disagree)."
    )
    # If disagreeing, the reason for disagreement
    response_reason_if_disagree: Optional[str] = Field(
        None, description="Reason for disagreement, if applicable."
    )
    # Date the response was served back to the filer
    response_service_date: Optional[str] = Field(
        None, description="Date the response was sent to you."
    )
    # How the response was served: 'Hand-delivery' or 'Mail'
    response_service_method: Optional[str] = Field(
        None, description="Method of service for the response: 'Hand-delivery' or 'Mail'."
    )
    # Address where the response was delivered or mailed
    response_service_address: Optional[str] = Field(
        None, description="Address where the response was delivered or mailed."
    )



class NoticeOfDismissal(BaseModel):
    # Name of the court location (e.g., 'Honolulu', 'Maui')
    division: Optional[str] = Field(
        None, description="Name of the court location (e.g., 'Honolulu', 'Maui')."
    )
    # Case number as found on court papers
    civil_number: Optional[str] = Field(
        None, description="Case number as found on your court papers."
    )
    # Full name(s) of plaintiff(s) (who started the case)
    plaintiffs: Optional[str] = Field(
        None, description="Full name(s) of the plaintiff(s) (person(s) suing)."
    )
    # Full name(s) of defendant(s) (person(s) being sued)
    defendants: Optional[str] = Field(
        None, description="Full name(s) of the defendant(s) (person(s) being sued)."
    )
    # Name and contact information for filing party (or their lawyer)
    filing_party_info: Optional[str] = Field(
        None, description="Your name and contact info (or your lawyer's info, if they are filing)."
    )
    # Scheduled court date and time (if any)
    court_date_and_time: Optional[str] = Field(
        None, description="Court date and time, if one is scheduled."
    )
    # Type of dismissal: 'WITH prejudice' or 'WITHOUT prejudice'
    dismissal_type: Optional[str] = Field(
        None, description="Type of dismissal: 'WITH prejudice' (case closed for good) or 'WITHOUT prejudice' (can refile)."
    )
    # Names of defendants being partially dismissed (if not dismissing entire case)
    partial_dismissal_defendants: Optional[str] = Field(
        None, description="Names of defendants to be dismissed, if not the entire case."
    )
    # Acknowledgment if all claims are dismissed
    no_remaining_claims_acknowledgment: Optional[str] = Field(
        None, description="Check this if all claims against all parties are dismissed."
    )
    # Date form is submitted to the court
    filing_date: Optional[str] = Field(
        None, description="Date when you submit this form to the court."
    )

    # Printed or typed name of the person filing
    printed_name: Optional[str] = Field(
        None, description="Print or type your full name under your signature."
    )


class OrderContinuingSmallClaimsCase(BaseModel):
    # Name of the court circuit (e.g., 'First Circuit', 'Second Circuit')
    circuit: Optional[str] = Field(
        None, description="Name of the court circuit (e.g., 'First Circuit', 'Second Circuit')."
    )
    # Specific division of the court (e.g., 'Honolulu', 'Waianae')
    division: Optional[str] = Field(
        None, description="Specific division of the court (e.g., 'Honolulu', 'Waianae')."
    )
    # Whether the order was issued in open court (at a hearing)
    filed_in_open_court: Optional[bool] = Field(
        False, description="Check if the order was issued in open court (at a hearing)."
    )
    # Name of the plaintiff (person who filed the case)
    plaintiff: Optional[str] = Field(
        None, description="Name of the plaintiff (person who filed the case)."
    )
    # Name of the defendant (person being sued)
    defendant: Optional[str] = Field(
        None, description="Name of the defendant (person being sued)."
    )
    # Court case number
    civil_number: Optional[str] = Field(
        None, description="Court case number (from your other court papers)."
    )
    # New hearing date (MM/DD/YYYY)
    new_court_date: Optional[str] = Field(
        None, description="New hearing date (MM/DD/YYYY)."
    )
    # New hearing time (12-hour format, e.g., '10:30')
    new_court_time: Optional[str] = Field(
        None, description="New hearing time (e.g., '10:30')."
    )
    # 'a.m.' or 'p.m.' for the hearing time
    time_of_day: Optional[str] = Field(
        None, description="Specify 'a.m.' or 'p.m.' for the hearing time."
    )
    # Courtroom number for the new hearing
    courtroom_number: Optional[str] = Field(
        None, description="Courtroom number for the new hearing."
    )
    # Date court clerk signed the order
    clerk_date: Optional[str] = Field(
        None, description="Date court clerk signed this order."
    )


class RequestForReliefFromCourtCosts(BaseModel):
    # Court circuit handling the case (e.g., 'First Circuit')
    circuit: Optional[str] = Field(
        None, description="Court circuit handling your case (e.g., 'First Circuit')."
    )
    # Specific court division (e.g., 'Honolulu', 'Maui')
    division: Optional[str] = Field(
        None, description="Specific court division (e.g., 'Honolulu', 'Maui')."
    )
    # Case number from court paperwork
    civil_number: Optional[str] = Field(
        None, description="Case number from your court paperwork."
    )
    # Name(s) of the person/people who started the case
    plaintiffs: Optional[str] = Field(
        None, description="Name(s) of the person or people who started the case."
    )
    # Name(s) of the person/people being sued
    defendants: Optional[str] = Field(
        None, description="Name(s) of the person or people being sued."
    )
    # Name and contact info of filing party (or attorney)
    filing_party_info: Optional[str] = Field(
        None, description="Your name and contact info, or your lawyer's if applicable."
    )
    # Check this if the attorney is pro bono (free)
    pro_bono_attorney_checkbox: Optional[bool] = Field(
        False, description="Check if attorney is working pro bono (for free)."
    )
    # 'Yes' or 'No' if you are employed
    is_employed: Optional[str] = Field(
        None, description="Write 'Yes' if you are working, or 'No' if not employed."
    )
    # Your monthly job income
    monthly_income: Optional[str] = Field(
        None, description="Total amount you earn each month from work."
    )
    # Name and address of current or most recent employer
    employer_name_and_address: Optional[str] = Field(
        None, description="Name and address of your current or last employer."
    )
    # Last date you were employed (if not currently working)
    date_last_employed: Optional[str] = Field(
        None, description="Last date you had a job (if not working now)."
    )
    # 'Rent' or 'Own' to describe housing
    housing_status: Optional[str] = Field(
        None, description="Write 'Rent' or 'Own' to show if you rent or own your home."
    )
    # Monthly payment for housing (rent or mortgage)
    monthly_housing_payment: Optional[str] = Field(
        None, description="Monthly payment for rent or mortgage."
    )
    # 'Yes' or 'No' if you receive rent assistance (e.g., Section 8)
    receives_rent_assistance: Optional[str] = Field(
        None, description="Write 'Yes' if you receive rent assistance, 'No' if not."
    )
    # 'Yes' or 'No' if you own other real estate
    owns_other_real_estate: Optional[str] = Field(
        None, description="Write 'Yes' if you own other real estate, 'No' if not."
    )
    # Value of other real estate, if any
    other_real_estate_value: Optional[str] = Field(
        None, description="Total value of other real estate (if applicable)."
    )
    # 'Yes' or 'No' if you have any bank accounts
    has_bank_account: Optional[str] = Field(
        None, description="Write 'Yes' if you have any bank accounts, 'No' if not."
    )
    # Total in all bank accounts, if any
    bank_account_total: Optional[str] = Field(
        None, description="Total amount in all bank accounts (if applicable)."
    )
    # 'Yes' or 'No' if you own any vehicles
    owns_vehicle: Optional[str] = Field(
        None, description="Write 'Yes' if you own any cars/trucks, 'No' if not."
    )
    # List of public assistance programs received (SSI, SNAP, TANF, etc.)
    receives_assistance: List[str] = Field(
        default_factory=list, description="List of assistance programs received (SSI, SNAP, TANF, etc.)."
    )
    # Dependents you support, with amount and relationship
    dependents: Optional[str] = Field(
        None, description="People you support financially and the amount for each."
    )
    # Any other income sources not listed above
    other_income_sources: Optional[str] = Field(
        None, description="Other sources of income (side jobs, gifts, etc.)."
    )
    # Date of applicant's signature
    declaration_signature_date: Optional[str] = Field(
        None, description="Date you sign this form."
    )

    # Printed or typed name under signature
    declaration_name: Optional[str] = Field(
        None, description="Print or type your full name under your signature."
    )
    # Judge's order: 'Granted' or 'Denied' (for judge only)
    court_order_result: Optional[str] = Field(
        None, description="For the judge: check 'Granted' (fees waived) or 'Denied' (you pay fees)."
    )
    # Date the judge signs the order (for judge only)
    judge_signature_date: Optional[str] = Field(
        None, description="Date the judge signs this form (judge only)."
    )



class SmallClaimsStatementOfClaimGeneral(BaseModel):
    # Name of the court division (e.g., 'Honolulu', 'Wai‘anae') where the case is filed
    division: Optional[str] = Field(
        None, description="Name of the court division where the case is filed."
    )
    # Case number (leave blank; court will fill this in)
    case_number: Optional[str] = Field(
        None, description="Case number (leave blank; court will assign)."
    )
    # Plaintiff's name, address, phone, and email
    plaintiff_contact: Optional[str] = Field(
        None, description="Plaintiff's name, address, phone, and email."
    )
    # Defendant's name, address, phone, and email
    defendant_contact: Optional[str] = Field(
        None, description="Defendant's name, address, phone, and email."
    )
    # Attorney info (if any): name, attorney number, firm, address, phone, email
    attorney_contact: Optional[str] = Field(
        None, description="Attorney information (leave blank if none)."
    )
    # Amount of money allegedly owed (must be $5,000 or less)
    amount_owed: Optional[str] = Field(
        None, description="Amount claimed owed (must be $5,000 or less)."
    )
    # Date money became owed (MM/DD/YYYY)
    date_money_owed_since: Optional[str] = Field(
        None, description="Date the money became owed (MM/DD/YYYY)."
    )
    # Reason and details for the claim
    reason_for_claim: Optional[str] = Field(
        None, description="Reason and explanation for the claim."
    )
    # Date plaintiff signs the declaration
    declaration_date: Optional[str] = Field(
        None, description="Date plaintiff signs the declaration."
    )

    # Defendant's name (again, for notice section)
    defendant_name_notice: Optional[str] = Field(
        None, description="Defendant's name for the notice section."
    )
    # Hearing location (court fills in)
    hearing_place: Optional[str] = Field(
        None, description="Hearing location (court fills in)."
    )
    # Hearing date and time (court fills in)
    hearing_date_time: Optional[str] = Field(
        None, description="Hearing date and time (court fills in)."
    )
    # Date court clerk scheduled the hearing (court fills in)
    clerk_signature_date: Optional[str] = Field(
        None, description="Date clerk scheduled the hearing (court fills in)."
    )


class SmallClaimsStatementOfClaimGeneralSecurityDeposit(BaseModel):
    # Name of the court division (e.g., 'Honolulu', 'Wai‘anae')
    division: Optional[str] = Field(
        None, description="Name of the court division where you're filing the case."
    )
    # Case number (leave blank; court will assign)
    case_number: Optional[str] = Field(
        None, description="Leave blank. Court will assign a case number."
    )
    # Plaintiff's full name (tenant)
    plaintiff_name: Optional[str] = Field(
        None, description="Your full name (the tenant)."
    )
    # Plaintiff's contact info: address, phone, email
    plaintiff_contact: Optional[str] = Field(
        None, description="Your full address, phone number, and email."
    )
    # Landlord's full name (defendant)
    landlord_name: Optional[str] = Field(
        None, description="Full name of your landlord (the defendant)."
    )
    # Landlord's contact info: address, phone, email (if known)
    landlord_contact: Optional[str] = Field(
        None, description="Landlord's full address, phone number, and email (if known)."
    )
    # Amount of security deposit believed owed
    amount_owed: Optional[str] = Field(
        None, description="Amount of your security deposit you believe is owed."
    )
    # Move-out date (MM/DD/YYYY)
    move_out_date: Optional[str] = Field(
        None, description="Date you moved out (MM/DD/YYYY)."
    )
    # Explanation for claim (can be multiple pages)
    reason_for_claim: Optional[str] = Field(
        None, description="Explanation for why you believe your landlord should return your security deposit."
    )
    # Date the declaration is signed
    declaration_date: Optional[str] = Field(
        None, description="Date you are signing this form."
    )
    # Landlord's name (again for notice section)
    notice_to: Optional[str] = Field(
        None, description="Your landlord’s name again for the notice section."
    )
    # Hearing place (court fills in)
    hearing_place: Optional[str] = Field(
        None, description="Court fills in with hearing location."
    )
    # Hearing date and time (court fills in)
    hearing_date_time: Optional[str] = Field(
        None, description="Court fills in with hearing date and time."
    )
    # Date clerk scheduled the hearing (court fills in)
    clerk_signature_date: Optional[str] = Field(
        None, description="Court clerk writes the date hearing was scheduled."
    )



class StipulationForDismissal(BaseModel):
    # Name of the court division (e.g., 'Honolulu', 'Waianae', etc.)
    division: Optional[str] = Field(
        None, description="Name of the court division where the case is handled."
    )
    # Civil case number (from court documents)
    civil_number: Optional[str] = Field(
        None, description="Case number for your court case."
    )
    # Full name(s) of Plaintiff(s)
    plaintiffs: Optional[str] = Field(
        None, description="Full name(s) of the Plaintiff(s)."
    )
    # Full name(s) of Defendant(s)
    defendants: Optional[str] = Field(
        None, description="Full name(s) of the Defendant(s)."
    )
    # Name and contact info of the filing party or attorney
    filing_party_info: Optional[str] = Field(
        None, description="Name and contact info of person or attorney submitting this form."
    )
    # Next court date and time, or 'None'
    next_court_date_time: Optional[str] = Field(
        None, description="Next court date and time, or 'None' if none scheduled."
    )
    # Type of next court event (Return, Pre-Trial, Trial, Answer, etc.)
    next_court_type: Optional[str] = Field(
        None, description="Type of next scheduled court event."
    )
    # Dismissal type: 'WITH prejudice' or 'WITHOUT prejudice'
    dismissal_type: Optional[str] = Field(
        None, description="Type of dismissal: 'WITH prejudice' or 'WITHOUT prejudice'."
    )
    # If partial dismissal, name(s) of defendant(s) being dismissed
    partial_dismissal_defendant: Optional[str] = Field(
        None, description="Names of defendant(s) if only some are being dismissed."
    )
    # Check this if all claims against all parties are being dismissed
    full_dismissal_confirmed: Optional[bool] = Field(
        False, description="Check if dismissing all claims against all parties (ending case completely)."
    )
    # Date Plaintiff (or attorney) signs the form
    plaintiff_signature_date: Optional[str] = Field(
        None, description="Date Plaintiff (or attorney) signs this form."
    )
    # Printed/typed name of Plaintiff or their lawyer
    plaintiff_printed_name: Optional[str] = Field(
        None, description="Printed/typed name of Plaintiff or their lawyer."
    )
    # Date Defendant (or attorney) signs the form
    defendant_signature_date: Optional[str] = Field(
        None, description="Date Defendant (or attorney) signs this form."
    )


user_forms = {
    "Certificate of Service": CertificateOfService,
    "Counterclaim": Counterclaim,
    "Non Hearing Motion for Continuance": NonHearingMotionForContinuance,
    "Notice of Dismissal": NoticeOfDismissal,
    "Order Continuing Small Claims Case": OrderContinuingSmallClaimsCase,
    "Request for Relief from Court Costs": RequestForReliefFromCourtCosts,
    "Small Claims - Statement of Claim - General": SmallClaimsStatementOfClaimGeneral,
    "Small Claims - Statement of Claim - Security Deposit": SmallClaimsStatementOfClaimGeneralSecurityDeposit,
    "Stipulation for Dismissal": StipulationForDismissal,
}
