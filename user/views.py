from django.shortcuts import render, redirect, get_object_or_404
from .models import Enfant, Groupe, Adresse, Etablissement
from .forms import EnfantForm, AdresseForm, GroupeForm
from .filters import EnfantFilter

MODELE_PAR_TYPE = {
    'enfant' : Enfant,
    'etablissement' : Etablissement,
    'groupe' : Groupe,
}

def donnees_list(request):
    filtre_enfant = EnfantFilter(request.GET, queryset=Enfant.objects.all())
    enfants_filtres = filtre_enfant.qs

    context = {"filtre" : filtre_enfant, "enfants" : enfants_filtres, "groupes" : Groupe.objects.all(), "etablissements" : Etablissement.objects.all()}
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

def enfant_edit(request, enfant_id):
    enfant = Enfant.objects.get(pk = enfant_id)
    adresse = enfant.adresse

    if request.method == 'POST':
        enfant_form = EnfantForm(request.POST, instance = enfant)
        adresse_form = AdresseForm(request.POST, instance = adresse)

        if enfant_form.is_valid() and adresse_form.is_valid():
            # Crée d'abord l'adresse
            adresse = adresse_form.save()

            # Crée l’enfant en associant l’adresse
            enfant = enfant_form.save(commit=False)
            enfant.adresse = adresse
            enfant.save()

            return redirect("donnees_list")
    else:
        enfant_form = EnfantForm(instance = enfant)
        adresse_form = AdresseForm(instance = adresse)

    return render(request, "user/enfant_edit.html", {
        "form": enfant_form,
        "adresse_form": adresse_form,
    })

def enfant_remove(request, enfant_id):
    enfant = Enfant.objects.get(pk = enfant_id)
    adresse = enfant.adresse
    enfant.delete()
    if adresse:
        adresse.delete()
    return redirect("donnees_list")

def groupe_add(request):
    if request.method == 'POST':
        form = GroupeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("donnees_list")
    else:
        form = GroupeForm()

    return render(request, "user/groupe_add.html", {"form": form})

def groupe_edit(request, groupe_id):
    groupe = Groupe.objects.get(pk = groupe_id)

    if request.method == 'POST':
        form = GroupeForm(request.POST, instance = groupe)
        if form.is_valid():
            form.save()
            return redirect("donnees_list")
    else:
        form = GroupeForm(instance = groupe)

    return render(request, "user/groupe_edit.html", {"form": form})

def groupe_remove(request, groupe_id):
    groupe = Groupe.objects.get(pk = groupe_id)
    groupe.delete()
    return redirect("donnees_list")
