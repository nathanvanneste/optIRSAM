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
        raise ValueError("OSRM n’a pas renvoyé les matrices attendues.")
    distMat = [[int(d) for d in row] for row in data["distances"]]
    durMat  = [[int(d) for d in row] for row in data["durations"]]
    return distMat, durMat

def format_solution(manager, routing, solution, distMat, durMat, group):
    """
    Retourne un dict sérialisable incluant pour chaque nœud:
      - vehicle_id
      - sequence de prénoms+nom
      - distance et durée totales
    """
    routes = []
    # liste des enfants pour mapper node→Enfant (0 = dépôt)
    enfants = list(group.enfants.all())
    for vid in range(routing.vehicles()):
        index = routing.Start(vid)
        seq, dist, dur = [], 0, 0
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            # 0 c’est le dépôt, sinon -1 pour accéder à enfants[node-1]
            if node == 0:
                seq.append("Dépôt")
            else:
                child = enfants[node-1]
                seq.append(f"{child.prenom} {child.nom}")
            nxt = solution.Value(routing.NextVar(index))
            nnode = manager.IndexToNode(nxt)
            dist += distMat[node][nnode]
            dur  += durMat[node][nnode]
            index = nxt
        # dernière position End
        seq.append("Fin")
        routes.append({
            "vehicle_id":     vid,
            "sequence":       seq,
            "total_distance": dist,
            "total_duration": dur
        })
    return {"status":"SUCCESS", "routes": routes}

def solve_vrp(group, etablissement, capacities, time_limit, calculation_mod, mode="closed"):
    # --- 1) Matrices OSRM ---
    coord_list = [
        f"{c.adresse.longitude},{c.adresse.latitude}"
        for c in group.enfants.all()
    ]
    depot = f"{etablissement.adresse.longitude},{etablissement.adresse.latitude}"
    coords = ";".join([depot] + coord_list)
    distMat, durMat = get_matrices(coords)

    # --- 2) Variables de base ---
    nb_nodes = len(distMat)
    num_veh  = len(capacities)
    depot_ix = 0

    # --- 3) Définir listes starts/ends selon mode ---
    if mode == "no_start":
        # pas de départ au dépôt : démarrage sur nœuds, fin au dépôt
        possible = list(range(1, nb_nodes))
        starts = [ possible[i] if i < len(possible) else depot_ix
                   for i in range(num_veh) ]
        ends   = [ depot_ix ] * num_veh

    elif mode == "no_return":
        # départ au dépôt, pas de retour : fin sur nœuds
        possible = list(range(1, nb_nodes))
        starts = [ depot_ix ] * num_veh
        ends   = [ possible[i] if i < len(possible) else depot_ix
                   for i in range(num_veh) ]

    else:  # "closed"
        starts = [ depot_ix ] * num_veh
        ends   = [ depot_ix ] * num_veh

    manager = pywrapcp.RoutingIndexManager(
        nb_nodes, num_veh, starts, ends
    )
    routing = pywrapcp.RoutingModel(manager)

    # --- 4) Coût distance/duration callback ---
    def cost_cb(i, j):
        ni = manager.IndexToNode(i)
        nj = manager.IndexToNode(j)
        return distMat[ni][nj] if calculation_mod == "Distance" else durMat[ni][nj]

    tc_index = routing.RegisterTransitCallback(cost_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(tc_index)

    # --- 5) Dimension capacité ---
    def demand_cb(i):
        return 0 if manager.IndexToNode(i) == depot_ix else 1

    dc_index = routing.RegisterUnaryTransitCallback(demand_cb)
    routing.AddDimensionWithVehicleCapacity(
        dc_index,
        0,
        capacities,      # liste de capacités par véhicule
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
    return format_solution(manager, routing, sol, distMat, durMat, group)
