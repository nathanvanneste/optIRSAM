from django.shortcuts import render, redirect, get_object_or_404
from .models import Enfant, Groupe, Adresse, Etablissement
from .forms import EnfantForm, AdresseForm

MODELE_PAR_TYPE = {
    'enfant' : Enfant,
    'etablissement' : Etablissement,
    'groupe' : Groupe,
}

def donnees_list(request):
    context = {"enfants" : Enfant.objects.all(), "groupes" : Groupe.objects.all(), "etablissements" : Etablissement.objects.all()}
    return render(request, 'user/donnees_list.html', context)

def infos(request, objet_type, objet_id):
    modele = MODELE_PAR_TYPE.get(objet_type.lower())
    objet = get_object_or_404(modele, id=objet_id)
    context = {"objet" : objet, "type" : objet_type.lower()}
    return render(request, "user/infos.html", context)


def enfant_add(request):
    if request.method == 'POST':
        enfant_form = EnfantForm(request.POST)
        adresse_form = AdresseForm(request.POST)

        if enfant_form.is_valid() and adresse_form.is_valid():
            # Crée d'abord l'adresse
            adresse = adresse_form.save()

            # Crée l’enfant en associant l’adresse
            enfant = enfant_form.save(commit=False)
            enfant.adresse = adresse
            enfant.save()

            return redirect("donnees_list")
    else:
        enfant_form = EnfantForm()
        adresse_form = AdresseForm()

    return render(request, "user/enfant_add.html", {
        "form": enfant_form,
        "adresse_form": adresse_form,
    })