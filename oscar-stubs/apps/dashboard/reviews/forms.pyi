from django import forms

class DashboardProductReviewForm(forms.ModelForm):
    status: forms.ChoiceField

    class Meta:
        model: type
        fields: tuple[str, ...]

class ProductReviewSearchForm(forms.Form):
    STATUS_CHOICES: tuple[tuple[str | int, str], ...]
    keyword: forms.CharField
    status: forms.ChoiceField
    date_from: forms.DateTimeField
    date_to: forms.DateTimeField
    name: forms.CharField
    def get_friendly_status(self) -> str: ...
