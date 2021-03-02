from django.core.exceptions import ValidationError

from django import forms
from django.utils import formats, timezone

from .fields import GroupedModelChoiceField
from .models import Issue, Deposit, Key, Person

import logging

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name',
                  'last_name',
                  'university_email',
                  'private_email',
                  'phone_number',
                  'group']

    def clean(self):
        cleaned_data = super().clean()
        university_email = cleaned_data.get("university_email")
        private_email = cleaned_data.get("private_email")

        logging.debug("MAIL CLEAN")
        logging.debug("{} - {}".format(university_email, private_email))

        if university_email == private_email:
            msg = "Private und Universitäts Mail dürfen nicht indentisch sein."
            self.add_error('university_email', "")
            self.add_error('private_email', "Bitte wählen Sie eine andere Mailadresse." )
            raise ValidationError(msg, "mails-not-identical")



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



class IssueForm(forms.ModelForm):
    key = GroupedModelChoiceField(
        queryset=Key.objects.not_currently_issued(stolen_or_lost=False), 
        choices_groupby='locking_system',
        label="Schlüssel"
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
        key = cleaned_data.get("key")
        logging.debug("Cleaned Key: {}".format(key))
        if key:
            if key.get_current_issue():
                raise ValidationError(("Schlüssel ist momentan \
                                        an {} verliehen".format(key.get_current_issue().person)),
                                        code='key-not-returned')
      


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
            raise ValidationError(('Bitte das Rückgabedatum angeben.'), code='required')

        if in_date < out_date:
            formated_date = formats.date_format(out_date)
            msg = 'Rückgabedatum muss nach dem {} (Ausgabedatum) liegen.'.format(formated_date)
            self.add_error('in_date', msg)
