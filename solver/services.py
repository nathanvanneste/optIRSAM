from math import ceil
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import requests

def get_matrices(coords, annotations=("distance","duration")):
    """
    Interroge OSRM pour obtenir les matrices distance & durée.
    Retourne (distMat, durMat) ou lève une exception.
    """
    base = "https://router.project-osrm.org/table/v1/driving/"
    url  = base + coords
    resp = requests.get(url, params={"annotations": ",".join(annotations)})
    resp.raise_for_status()
    data = resp.json()
    if "distances" not in data or "durations" not in data:
        raise ValueError("OSRM n'a pas renvoyé les matrices attendues.")
    distMat = [[int(d) for d in row] for row in data["distances"]]
    durMat  = [[int(d) for d in row] for row in data["durations"]]
    return distMat, durMat

def format_solution(manager, routing, solution, distMat, durMat, group,
                    virtual_start=False, virtual_end=False):
    """
    Retourne un dict sérialisable incluant pour chaque nœud:
      - vehicle_id
      - sequence de prénoms+nom
      - distance et durée totales

    Si virtual_start/end est True, les nœuds virtuels sont ignorés dans l'affichage.
    """
    routes = []
    enfants = list(group.enfants.all())

    for vid in range(routing.vehicles()):
        index = routing.Start(vid)
        seq, dist, dur = [], 0, 0
        route_started = False

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)

            is_virtual_start = virtual_start and node == 0
            is_virtual_end   = virtual_end and node == len(distMat) - 1

            # Ignorer le dépôt virtuel en début
            if not is_virtual_start and not is_virtual_end:
                route_started = True
                if node == 0:
                    seq.append("Dépôt")
                else:
                    child = enfants[node - 1] if not virtual_start else enfants[node - 1]
                    seq.append(f"{child.prenom} {child.nom}")

            # Calculer le coût même sur arc virtuel (ou pas, à toi de décider)
            nxt = solution.Value(routing.NextVar(index))
            nnode = manager.IndexToNode(nxt)

            if not is_virtual_end:
                dist += distMat[node][nnode]
                dur  += durMat[node][nnode]

            index = nxt

        # Fin de tournée
        if virtual_end:
            seq.append("Fin (libre)")
        else:
            seq.append("Fin")

        routes.append({
            "vehicle_id":     vid,
            "sequence":       seq,
            "total_distance": dist,
            "total_duration": dur
        })

    return {"status": "SUCCESS", "routes": routes}


def solve_vrp(groupe, etablissement, capacities, time_limit, calculation_mod, mode="closed"):
    #Levée d'exception
    if not etablissement.adresse or not etablissement.adresse.latitude or not etablissement.adresse.longitude:
        raise ValueError("L’établissement n’a pas de coordonnées valides.")

    for enfant in groupe.enfants.all():
        if not enfant.adresse or not enfant.adresse.latitude or not enfant.adresse.longitude:
            raise ValueError(f"L'enfant {enfant} n’a pas de coordonnées géographiques.")
    # --- 1) Coordonnées OSRM ---
    coord_list = [
        f"{c.adresse.longitude},{c.adresse.latitude}"
        for c in groupe.enfants.all()
    ]
    depot = f"{etablissement.adresse.longitude},{etablissement.adresse.latitude}"
    coords_list = [depot] + coord_list

    # --- 1.1) Modifications virtuelles selon le mode ---
    virtual_start = False
    virtual_end = False

    if mode == "no_start":
        virtual_start = True
        coords_list = ["0,0"] + coords_list  # dépôt virtuel fictif

    elif mode == "no_end":
        virtual_end = True
        coords_list = coords_list + ["0,0"]  # dépôt virtuel fictif

    coords = ";".join(coords_list)
    distMat, durMat = get_matrices(coords)

    # --- 1.2) Adapter la matrice si dépôt virtuel ---
    if virtual_start:
        # Ligne en plus au début avec zéros vers tous les nœuds (sauf soi-même)
        row = [0] * len(distMat[0])
        distMat.insert(0, row)
        durMat.insert(0, row.copy())
        for r in distMat[1:]:
            r.insert(0, 999999)  # Interdire retour vers dépôt virtuel
        for r in durMat[1:]:
            r.insert(0, 999999)
        depot_ix = 0
        offset = 1
    else:
        depot_ix = 0
        offset = 0

    if virtual_end:
        # Colonne en plus à la fin avec zéros depuis tous les nœuds
        for r in distMat:
            r.append(0)
        for r in durMat:
            r.append(0)
        end_index = len(distMat) - 1
    else:
        end_index = depot_ix

    # --- 2) Variables de base ---
    nb_nodes = len(distMat)
    num_veh  = len(capacities)

    # --- 3) Définir starts/ends ---
    if virtual_start:
        starts = [0] * num_veh
    else:
        starts = [depot_ix] * num_veh

    if virtual_end:
        ends = [end_index] * num_veh
    else:
        ends = [depot_ix] * num_veh

    manager = pywrapcp.RoutingIndexManager(
        nb_nodes, num_veh, starts, ends
    )
    routing = pywrapcp.RoutingModel(manager)

    # --- 4) Callback de coût ---
    def cost_cb(i, j):
        ni = manager.IndexToNode(i)
        nj = manager.IndexToNode(j)
        return distMat[ni][nj] if calculation_mod == "Distance" else durMat[ni][nj]

    tc_index = routing.RegisterTransitCallback(cost_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(tc_index)

    # --- 5) Dimension capacité ---
    def demand_cb(i):
        ni = manager.IndexToNode(i)
        return 0 if ni == depot_ix or (virtual_start and ni == 0) else 1

    dc_index = routing.RegisterUnaryTransitCallback(demand_cb)
    routing.AddDimensionWithVehicleCapacity(
        dc_index,
        0,
        capacities,
        True,
        "capacity"
    )

    # --- 6) Paramètres de recherche ---
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
    )
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_params.time_limit.seconds = time_limit

    # --- 7) Solve ---
    sol = routing.SolveWithParameters(search_params)
    if not sol:
        return {"status": "FAILURE", "routes": []}

    # --- 8) Formatage final avec noms d'enfants ---
    return format_solution(manager, routing, sol, distMat, durMat, groupe)
