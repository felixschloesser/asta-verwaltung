from dateutil.relativedelta import relativedelta

from gdpr.purposes.default import AbstractPurpose

class GeneralPurpose(AbstractPurpose):
    name = "Ausleihenverwaltung"
    slug = "issue_management"
    expiration_timedelta = relativedelta(years=4)
    fields = "__SELF__"  # Delte my model


class BorrowersCommunciactionPurpose(AbstractPurpose):
    name = "Kommunikation mit Entleihenden"
    slug = "communicating_with_borrowers"
    expiration_timedelta = relativedelta(years=2)
    fields = [
        "private_email",
        "university_email",
        "phone_number",         
    ]  # Anonymize only these fields as defined in anonymizer