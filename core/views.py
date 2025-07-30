from django.shortcuts import render

def lancement(request):
    return render(request, "core/lancement.html")

def accueil(request):
    return render(request, "core/accueil.html")