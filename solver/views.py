from django.shortcuts import render, redirect
from .forms import RunForm

def parametrage(request):
    return render(request, 'solver/parametrage.html')

def run_create(request):
    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid():
            run = form.save(commit = False)
            run.status = 'RUNNING'
            run.save()
            # 1) Prendre les enfants du groupe, construire les données
            # 2) Appeler OrTools ici ou déclencher un task Celery
            # 3)Mettre à jour run.result_json et run.status
            return redirect('run_detail', pk = run.pk)
    else:
        form = RunForm()
    return render(request, 'solver/run_form.html',{'form' : form})
