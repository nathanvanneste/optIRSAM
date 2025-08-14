import folium
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
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
    run = get_object_or_404(Run, pk=pk)

    # Charger les données JSON
    data = json.loads(run.result_json)

    # Enfants et établissement
    enfants = list(run.groupe.enfants.all())
    etab = run.etablissement
    etab_coords = (etab.adresse.latitude, etab.adresse.longitude)

    # Coords enfants pour centrage carte
    coords = [(e.adresse.latitude, e.adresse.longitude) for e in enfants]
    if etab_coords:
        coords.append(etab_coords)

    # Centrage carte
    if coords:
        moy_lat = sum(c[0] for c in coords) / len(coords)
        moy_lon = sum(c[1] for c in coords) / len(coords)
    else:
        moy_lat, moy_lon = 43.3, 5.4  # fallback (Marseille par ex)

    m = folium.Map(location=[moy_lat, moy_lon], zoom_start=11)

    # Établissement
    folium.Marker(
        location=etab_coords,
        popup="Établissement",
        icon=folium.Icon(color="green", icon="home")
    ).add_to(m)

    # Routes optimisées
    for route in data.get("routes", []):
        points = []
        for name in route["sequence"]:
            if name in ["Fin", "Fin (libre)"]:
                continue
            elif name == "Établissement":
                points.append(etab_coords)
            else:
                # Nom = "Prénom Nom" → retrouver l’enfant
                for e in enfants:
                    if f"{e.prenom} {e.nom}" == name:
                        points.append((e.adresse.latitude, e.adresse.longitude))
                        break

        # Lignes + marqueurs
        if points:
            folium.PolyLine(points, color="blue", weight=4).add_to(m)
            for lat, lon in points:
                folium.CircleMarker(location=(lat, lon), radius=4, color="red", fill=True).add_to(m)

    # Convertir carte → HTML
    map_html = m._repr_html_()

    return render(request, 'solver/run_detail.html', {
        'run': run,
        'map': map_html
    })

def download_excel(request, pk):
    run = get_object_or_404(Run, pk=pk)

    # Charger les données JSON
    data = json.loads(run.result_json)

    # Générer le fichier Excel
    excel_file = export_to_excel_formatted(data)

    # On va nettoyer le nom du fichier excel qui ne peut contenir certains caractère
    nom_sans_extension = nettoyage_nom_excel(data["routes"][0]["nom_tournee"])


    # Création du nom de fichier final
    filename = f"{nom_sans_extension}.xlsx"

    # Retourner le fichier en téléchargement
    return FileResponse(
        excel_file,
        as_attachment=True,
        filename=filename,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )