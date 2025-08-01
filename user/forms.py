from django import forms
from .models import Enfant, Adresse, Etablissement

class EnfantForm(forms.ModelForm):
    etablissement = forms.ModelChoiceField(queryset = Etablissement.objects.all(), label = "Etablissement")
    class Meta:
        model = Enfant
        fields = ['prenom','nom','etablissement']
        labels = {'prenom' : 'Prénom', 'nom' : 'Nom'}

class AdresseForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = ['num_et_rue', 'ville', 'code_postal', 'latitude', 'longitude']
        labels = {'num_et_rue' : 'Numéro et libellé de la voie', 'ville' : 'Ville', 'code_postal' : 'Code postal', 'latitude' : 'Latitude', 'longitude': 'Longitude'}
    
