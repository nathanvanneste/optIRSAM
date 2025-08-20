from django.shortcuts import render

# Contrôleurs on ne peut plus simples, ce sont des pages avec uniquement des redirections tout se fait après en HTML 
def lancement(request):
    return render(request, "core/index.html")

def accueil(request):
    return render(request, "core/accueil.html")