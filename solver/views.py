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
            if run.vehicules == 'VOITURES':
                capacities = [4]*nb_enfants
            elif run.vehicules == 'VANS':
                capacities = [8]*nb_enfants
            else:
                capacities = [4,8]*nb_enfants
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

    # Centrage carte sur l'établissement
    if etab_coords:
        center_lat, center_lon = etab_coords
    else:
        center_lat, center_lon = 43.3, 5.4  # fallback (Marseille par ex)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

    # Établissement
    folium.Marker(
        location=etab_coords,
        popup=f"<b>{etab.nom}</b><br>{etab.adresse}",
        tooltip=f"{etab.nom}",
        icon=folium.Icon(color="green", icon="home")
    ).add_to(m)

    # Couleurs différentes pour chaque tournée
    colors = ['red', 'blue', 'purple', 'orange', 'darkred', 'lightred', 
              'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 
              'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

    # Routes optimisées
    for route_idx, route in enumerate(data.get("routes", [])):
        # Couleur pour cette tournée (cyclique si plus de tournées que de couleurs)
        route_color = colors[route_idx % len(colors)]
        
        points = []
        points_info = []  # Pour stocker les infos de chaque point
        
        for i, name in enumerate(route["sequence"]):
            if name in ["Fin", "Fin (libre)"]:
                continue
            elif name == "Établissement":
                points.append(etab_coords)
                points_info.append({
                    'coords': etab_coords,
                    'name': f"{etab.nom}",
                    'type': 'etablissement'
                })
            else:
                # Nom = "Prénom Nom" → retrouver l'enfant
                for e in enfants:
                    if f"{e.prenom} {e.nom}" == name:
                        enfant_coords = (e.adresse.latitude, e.adresse.longitude)
                        points.append(enfant_coords)
                        points_info.append({
                            'coords': enfant_coords,
                            'name': f"{e.prenom} {e.nom}",
                            'adresse': f"{e.adresse.num_et_rue}, {e.adresse.ville}",
                            'type': 'enfant'
                        })
                        break

        # Ligne de la tournée avec couleur spécifique
        if points:
            folium.PolyLine(
                points, 
                color=route_color, 
                weight=4, 
                opacity=0.8,
                popup=f"<b>Tournée {route_idx + 1}</b><br>Distance: {route['distance_totale']}<br>Durée: {route['duree_totale']}"
            ).add_to(m)
            
            # Marqueurs pour chaque point avec tooltips
            for point_info in points_info:
                if point_info['type'] == 'etablissement':
                    # L'établissement garde son marqueur maison vert
                    continue  # Déjà ajouté plus haut
                else:
                    # Marqueurs colorés pour les enfants
                    folium.CircleMarker(
                        location=point_info['coords'],
                        radius=6,
                        popup=f"<b>{point_info['name']}</b><br>{point_info['adresse']}<br><i>Tournée {route_idx + 1}</i>",
                        tooltip=point_info['name'],
                        color='white',
                        fillColor=route_color,
                        weight=2,
                        fillOpacity=0.8
                    ).add_to(m)

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