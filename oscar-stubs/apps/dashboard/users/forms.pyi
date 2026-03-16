from django import forms

class UserSearchForm(forms.Form):
    email: forms.CharField
    name: forms.CharField

class ProductAlertUpdateForm(forms.ModelForm):
    class Meta:
        model: type
        fields: list[str]

class ProductAlertSearchForm(forms.Form):
    STATUS_CHOICES: tuple[tuple[str | int, str], ...]
    status: forms.ChoiceField
    name: forms.CharField
    email: forms.EmailField
