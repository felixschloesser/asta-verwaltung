from django.core.exceptions import ValidationError

from django import forms
from django.utils import formats, timezone

from .models import Issue, Deposit, Key, Person
from .fields import GroupedModelChoiceField
from .widgets import Datalist

import logging

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name',
                  'last_name',
                  'university_email',
                  'private_email',
                  'phone_number',
                  'group',
                  'comment',
                  'gdpr_consent']

        widgets = {
            'first_name': forms.TextInput(attrs={'required':'true', 'placeholder': "Erika"}),
            'last_name': forms.TextInput(attrs={'required':'true', 'placeholder': "Mustermann"}),
            'university_email': forms.EmailInput(attrs={'required':'true', 'placeholder': "erika.mustermann@tuhh.de"}),
            'private_email': forms.EmailInput(attrs={'required':'true', 'placeholder': "erika.mustermann@gmx.de"}),
            'phone_number': forms.NumberInput(attrs={'required':'true', 'placeholder': "0170 1234567"}),
            'comment': forms.Textarea(attrs={'required':'true', 'cols': 80, 'rows': 3, 'placeholder': "Optionaler Kommentar...", 'spellcheck': 'true', 'lang': 'de-DE'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        university_email = cleaned_data.get("university_email")
        private_email = cleaned_data.get("private_email")
        gdpr_consent = cleaned_data.get("gdpr_consent")

        logging.debug("Checking if mail adresses are not identical...")
        logging.debug("{}, {}".format(university_email, private_email))

        if university_email == private_email:
            logging.warning("university_email and private_email can't be identical: {}".format(private_email))

            msg = "Private- und Unimail dürfen nicht indentisch sein."
            self.add_error('university_email', "")
            self.add_error('private_email', "Bitte wählen Sie eine andere Mailadresse." )
            raise ValidationError(msg, "mails-not-identical")

        if not gdpr_consent:
            logging.warning("need to consent to gdpr statement")
            self.add_error('gdpr_consent', "Die Zustimmung ist auf Grund der Datenschutz-Grundverordnung notwendig." )



class DepositCreateForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount',
                  'currency',
                  'in_method',
                  'comment']

        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': "Optionaler Kommentar zur Entgegennahme...", 'spellcheck': 'true', 'lang': 'de-DE'}),
        }



class DepositRetainForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'required':'true', 'cols': 80, 'rows': 3, 'placeholder': "Begründung für die Einbehaltung...", 'spellcheck': 'true', 'lang': 'de-DE'}),
        }



class DepositReturnForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['out_method',
                  'comment']

        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': "Optionaler Kommentar zur Rückgabe...", 'spellcheck': 'true', 'lang': 'de-DE'}),
        }



class KeyLostForm(forms.ModelForm):
    class Meta:
        model = Key
        fields = ['stolen_or_lost',
                  'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': "Optionaler Kommentar zur Verlust...", 'spellcheck': 'true', 'lang': 'de-DE'}),
        }


class KeyFoundForm(forms.ModelForm):
    class Meta:
        model = Key
        fields = ['stolen_or_lost',
                  'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3, 'placeholder': "Optionaler Kommentar zur Wiederauftauchen...", 'spellcheck': 'true', 'lang': 'de-DE'}),
        }


class IssueForm(forms.ModelForm):
    key = forms.ModelChoiceField(
        queryset=Key.objects.not_currently_issued(stolen_or_lost=False),
        label="Schlüssel",
        widget = Datalist(attrs={'required':'required'})
    )

    class Meta:
        model= Issue
        fields = ['key',
                  'out_date',
                  'active',
                  'comment',]
        widgets = {
            'out_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        logging.debug(cleaned_data)
        key = cleaned_data.get("key")
        if key and key.get_current_issue():
                raise ValidationError(("Schlüssel ist momentan \
                                        an {} verliehen".format(key.get_current_issue().person)),
                                        code='key-not-returned')
                logging.warning("Key {} already issued to".format(key, get_current_issue().person))



class IssueReturnForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['in_date',
                  'comment']


        widgets = {
            'in_date': forms.widgets.DateInput(attrs={'type': 'date', 'required':'required'}),
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        in_date = cleaned_data.get("in_date")
        out_date = self.instance.out_date

        if not in_date:
            logging.warning("out_date is required.")
            raise ValidationError(('Bitte das Rückgabedatum angeben.'), code='required')

        if in_date < out_date:
            logging.warning("in_date needs to be before out_date")
            formated_date = formats.date_format(out_date)
            msg = 'Rückgabedatum muss nach dem {} (Ausgabedatum) liegen.'.format(formated_date)
            self.add_error('in_date', msg)

