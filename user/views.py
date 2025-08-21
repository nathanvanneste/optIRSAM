from django.shortcuts import render, redirect, get_object_or_404

from .models import Enfant, Groupe, Etablissement
from .forms import EnfantForm, AdresseForm, GroupeForm

# Sert dans le contrôleur infos pour que la templates reconnaisse les corespondances
MODELE_PAR_TYPE = {
    'enfant' : Enfant,
    'etablissement' : Etablissement,
    'groupe' : Groupe,
}

# Donne du contexte dans la requête pour pouvoir passer et afficher les enfants, groupe, etablissement ect... Le filtrage se fait en JS sur la template (plus puissant)
def donnees_list(request):
    context = {
        "enfants": Enfant.objects.all(),
        "groupes": Groupe.objects.all(),
        "etablissements": Etablissement.objects.all()

    }
    return render(request, 'user/donnees_list.html', context)

# Reconnait le type d'objet et le passe à la template qui ajustera l'affichage en fonction du type 
def infos(request, objet_type, objet_id):
    modele = MODELE_PAR_TYPE.get(objet_type.lower())
    objet = get_object_or_404(modele, id=objet_id)
    context = {"objet" : objet, "type" : objet_type.lower()}
    return render(request, "user/infos.html", context)

# Méthode d'ajout d'enfant qui agit avec le formulaire
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

# Méthode d'édition d'enfant
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

# Méthode pour la suppression des enfants
def enfant_remove(request, enfant_id):
    enfant = get_object_or_404(Enfant, id=enfant_id)

    # Sauvegarde l'adresse associée
    adresse = enfant.adresse  

    # Supprime d'abord l'enfant
    enfant.delete()

    # Puis supprime l'adresse si elle existe et qu'elle n'est plus liée à d'autres enfants
    if adresse and not adresse.enfants.exists():
        adresse.delete()

    return redirect("donnees_list")

# Permet de créer un nouvel enfant en changeant le tutueur
def enfant_duplicate(request, enfant_id):
    # Récupère l'enfant à dupliquer
    enfant_original = get_object_or_404(Enfant, id=enfant_id)
    
    if request.method == 'POST':
        enfant_form = EnfantForm(request.POST)
        adresse_form = AdresseForm(request.POST)

        if enfant_form.is_valid() and adresse_form.is_valid():
            # Crée d'abord l'adresse
            adresse = adresse_form.save()

            # Crée l'enfant en associant l'adresse
            enfant = enfant_form.save(commit=False)
            enfant.adresse = adresse
            enfant.save()

            return redirect("donnees_list")
    else:
        # Prérempli les données avec celles de l'enfant original
        initial_enfant_data = {
            'nom': enfant_original.nom,
            'prenom': enfant_original.prenom,
            'etablissement': enfant_original.etablissement,
            'tuteur': '',
        }
        enfant_form = EnfantForm(initial=initial_enfant_data)
        adresse_form = AdresseForm()

    return render(request, "user/enfant_duplicate.html", {
        "form": enfant_form,
        "adresse_form": adresse_form,
        "enfant_original": enfant_original,
    })

# Méthode d'ajout d'un groupe 
def groupe_add(request):
    
    if request.method == 'POST':
        form = GroupeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("donnees_list")
    else:
        form = GroupeForm()

    return render(request, "user/groupe_add.html", {
        "form": form,
        "etablissements": Etablissement.objects.all()
    })

# Méthode d'édition d'un groupe 
def groupe_edit(request, groupe_id):
    groupe = Groupe.objects.get(pk = groupe_id)

    if request.method == 'POST':
        form = GroupeForm(request.POST, instance = groupe)
        if form.is_valid():
            form.save()
            return redirect("donnees_list")
    else:
        form = GroupeForm(instance = groupe)

    return render(request, "user/groupe_edit.html", {"form": form, "etablissements": Etablissement.objects.all()})

# Méthode de suppression d'un groupe 
def groupe_remove(request, groupe_id):
    groupe = Groupe.objects.get(pk = groupe_id)
    groupe.delete()
    return redirect("donnees_list")
