from django import forms
from .models import Run

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ['groupe', 'etablissement', 'calculation_mod','mode','capacity', 'time_limit']
        labels = {'groupe' : 'Groupe', 'etablissement' : 'Etablissement', 'calculation_mod' : 'Paramètre de coût', 'mode' : 'Depôt', 'capacity' : 'Capacité des véhicules', 'time_limit' : 'Temps de résolution'}