from django import forms

class ReportForm(forms.Form):
    report_type: forms.ChoiceField
    date_from: forms.DateField
    date_to: forms.DateField
    download: forms.BooleanField
