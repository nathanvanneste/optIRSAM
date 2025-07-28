from django import forms
from .models import Enfant, Groupe

class EnfantForm(forms.ModelForm):
    class Meta:
        model = Enfant
        fields = ['prenom','nom','adresse','etablissement']

class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['nom', 'enfants']