from django import forms
from .models import Run

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ['groupe', 'etablissement', 'calculation_mod','capacity', 'time_limit']