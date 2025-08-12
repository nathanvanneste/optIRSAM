from django import forms
from .models import Enfant, Adresse, Etablissement, Groupe


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
    
class GroupeForm(forms.ModelForm):
    enfants = forms.ModelMultipleChoiceField(
        queryset=Enfant.objects.none(),  # queryset vide par défaut
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
        fields = ['nom', 'enfants']
        labels = {'nom': 'Nom du Groupe'}

    def __init__(self, *args, **kwargs):
        # On récupère la queryset dynamique passée en kwargs
        enfants_queryset = kwargs.pop('enfants_queryset', None)
        super().__init__(*args, **kwargs)
        if enfants_queryset is not None:
            self.fields['enfants'].queryset = enfants_queryset
        else:
            self.fields['enfants'].queryset = Enfant.objects.all()
