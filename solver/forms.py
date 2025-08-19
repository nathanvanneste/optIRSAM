from django import forms
from .models import Run

class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ['groupe', 'calculation_mod','mode','vehicules', 'time_limit']
        labels = {'groupe' : 'Groupe', 'etablissement' : 'Etablissement', 'calculation_mod' : 'Calcul selon', 'mode' : 'Trajets', 'vehicules' : 'Type(s) des véhicules', 'time_limit' : 'Temps de résolution'}