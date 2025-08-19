from django import forms
from .models import Enfant, Adresse, Etablissement, Groupe


class EnfantForm(forms.ModelForm):
    etablissement = forms.ModelChoiceField(
        queryset=Etablissement.objects.all(), 
        label="Etablissement"
    )

    tuteur = forms.CharField(
        label="Tuteur",
        widget=forms.TextInput(attrs={'list': 'tuteur-options'})
    )

    class Meta:
        model = Enfant
        fields = ['prenom', 'nom', 'tuteur', 'etablissement']
        labels = {'prenom': 'Prénom', 'nom': 'Nom', 'tuteur': 'Tuteur'}
        
class AdresseForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = ['num_et_rue', 'ville', 'code_postal', 'latitude', 'longitude']
        labels = {'num_et_rue' : 'Numéro et libellé de la voie', 'ville' : 'Ville', 'code_postal' : 'Code postal', 'latitude' : 'Latitude', 'longitude': 'Longitude'}
    
class GroupeForm(forms.ModelForm):
    enfants = forms.ModelMultipleChoiceField(
        queryset=Enfant.objects.all(),
        label="Enfants du groupe",
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-checkbox-list',
                'style': 'max-height:200px; overflow-y:auto; border:1px solid #ccc; padding:10px; display:block;'
            }
        )
    )
    class Meta:
        model = Groupe
        fields = ['nom', 'etablissement', 'enfants']
        labels = {'nom': 'Nom du Groupe', 'etablissement' : 'Etablissement'}
