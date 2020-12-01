from django.core.exceptions import ValidationError

from django import forms
from django.utils import formats

from .models import Issue, Deposit

import datetime

class DepositCreateForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount',
                  'currency',
                  'in_datetime',
                  'in_method']

    initial= {'amount': 50.0,
              'in_datetime': datetime.datetime.now()}

# Custom Forms
class IssueReturnForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['in_date']

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

