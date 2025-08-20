from django import forms
from .models import Run

# Formulaire créer à partir du modèle RUN, permet de paramètrer une résolution
class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        # On ne met pas établissement car il est récuperé dans le contrôleur à partir de groupe
        fields = ['groupe', 'calculation_mod','mode','vehicules', 'time_limit']
        labels = {'groupe' : 'Groupe', 'calculation_mod' : 'Calcul selon', 'mode' : 'Trajets', 'vehicules' : 'Type(s) des véhicules', 'time_limit' : 'Temps de résolution'}