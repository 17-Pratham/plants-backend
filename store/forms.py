from django import forms
from .models import ProductFAQ

class ProductFAQBulkForm(forms.ModelForm):
    question_1 = forms.CharField(required=False)
    answer_1 = forms.CharField(widget=forms.Textarea, required=False)

    question_2 = forms.CharField(required=False)
    answer_2 = forms.CharField(widget=forms.Textarea, required=False)

    question_3 = forms.CharField(required=False)
    answer_3 = forms.CharField(widget=forms.Textarea, required=False)

    question_4 = forms.CharField(required=False)
    answer_4 = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = ProductFAQ
        fields = ['product']