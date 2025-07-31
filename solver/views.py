from django.shortcuts import render

def parametrage(request):
    return render(request, 'solver/parametrage.html')
