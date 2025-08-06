from django import forms
from .models import Run

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ['groupe', 'etablissement', 'calculation_mod','mode','capacity', 'time_limit']