import datetime

# Create your validators here.
def validate_university_mail(value):
    if "@tuhh.de" in value:
        return value
    else:
        raise ValidationError("Bitte die @tuhh.de-Adresse angeben.")


def present_or_future_date(value):
    try:
        # Convert if datetime
        date = value.date()
    except AttributeError:
        date = value


    if date >= datetime.date.today():
        # Date lies in the future
        return date
    else:
        raise ValidationError("Datum darf nicht in der Verangenheit liegen.")

def present_or_past_date(value):
    try:
        # Convert if datetime
        date = value.date()
    except AttributeError:
        date = value


    if date <= datetime.date.today():
        # Date lies in the past
        return date
    else:
        raise ValidationError("Datum darf nicht in der Zukunft liegen.")


def present_or_max_10_days_ago(value):
    try:
        # Convert if datetime
        date = value.date()
    except AttributeError:
        date = value

    if date <= datetime.date.today():
        if date > (datetime.date.today() - datetime.timedelta(days=10)):
            date
        else:
            raise ValidationError("Datum darf nicht länger als 10 Tage in der Verangenheit liegen.")
    else:
        raise ValidationError("Datum darf nicht in der Zukunft liegen.")

def present_or_max_3_days_ago(value):
    try:
        # Convert if datetime
        date = value.date()
    except AttributeError:
        date = value

    if date <= datetime.date.today():
        if date > (datetime.date.today() - datetime.timedelta(days=3)):
            date
        else:
            raise ValidationError("Datum darf nicht länger als 3 Tage in der Verangenheit liegen.")
    else:
        raise ValidationError("Datum darf nicht in der Zukunft liegen.")
