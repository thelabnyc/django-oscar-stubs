from django import forms

class PageSearchForm(forms.Form):
    title: forms.CharField

class PageUpdateForm(forms.ModelForm):
    url: forms.RegexField
    def clean_url(self) -> str: ...

    class Meta:
        model: type
        fields: tuple[str, ...]
