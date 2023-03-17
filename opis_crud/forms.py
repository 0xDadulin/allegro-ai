from django import forms
from hr_helper.models import Opis

class OpisForm(forms.ModelForm):
    class Meta:
        model = Opis
        fields = ['title', 'text']