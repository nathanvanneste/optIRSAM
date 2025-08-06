import json
from django.shortcuts import render, redirect, get_object_or_404
from .models import Run
from .forms import RunForm
from .services import *

def run_create(request):
    if request.method == 'POST':
        form = RunForm(request.POST)
        if form.is_valid():
            run = form.save(commit = False)
            run.status = 'RUNNING'
            run.save()
            nb_enfants = run.groupe.enfants.count()
            capacite_taxi = run.capacity
            capacities = [capacite_taxi]*nb_enfants
            result_python = solve_vrp(run.groupe, run.etablissement, capacities, run.time_limit, run.calculation_mod, run.mode)
            run.status = result_python["status"]
            run.result_json = json.dumps(result_python, indent = 2, ensure_ascii = False)
            run.save()
            return redirect('run_detail', pk = run.pk)
    else:
        form = RunForm()
    return render(request, 'solver/parametrage.html',{'form' : form})

def run_detail(request, pk):
    run = get_object_or_404(Run, pk = pk)
    return render(request, "solver/run_detail.html", {'run' : run})