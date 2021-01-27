from django.core.exceptions import ValidationError

from django import forms
from django.utils import formats, timezone

from .models import Issue, Deposit, Key

import logging


class DepositCreateForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount',
                  'currency',
                  'in_method',
                  'comment']

        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }

class DepositReturnForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['out_method']


class IssueForm(forms.ModelForm):
    class Meta:
        model= Issue
        fields = ['key',
                  'out_date',
                  'active',
                  'comment',]
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['key'].queryset = Key.all_keys.availible()

    def clean(self):
        cleaned_data = super().clean()
        key = cleaned_data.get("key")
        if key:
            current_issue = key.get_current_issue()
            if current_issue:
                raise ValidationError(("Schlüssel ist momentan \
                                        an {} verliehen".format(current_issue.person)),
                                        code='key-not-returned')



class IssueReturnForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['in_date',
                  'active']


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
