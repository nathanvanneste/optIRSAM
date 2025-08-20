from django.db import models
from user.models import Groupe, Etablissement

class Run(models.Model):
    # Groupe d'usagers sur lesquels sont lancés la résolution
    groupe = models.ForeignKey(Groupe, on_delete = models.CASCADE, related_name = 'runs')
    # Etablissement auquel appartiennent les usagers du groupe, récupérable via groupe.etablissement mais + pratique de le mettre en attribut
    etablissement = models.ForeignKey(Etablissement, on_delete = models.CASCADE, related_name = 'runs', null=True, blank=True)
    # Permet de définir par la suite la capacité
    vehicules = models.CharField(max_length = 50, choices = [('VOITURES','Voitures (5 places)'),('VANS','Vans (9 places)'),('VOITURES_ET_VANS','Voitures et vans')], default = 'VOITURES')
    # Temps accordé à la résolution après avoir trouvé une première solution
    time_limit = models.PositiveIntegerField(help_text = "en secondes")
    # Permettra de définir ce qu'on choisit dans la fonction collback de coût
    calculation_mod = models.CharField(max_length = 10, choices = [('DISTANCE','La distance'),('DURATION','La durée')], default = 'DISTANCE')
    # Va permettre de créer ou non des dépôt virtuel, selon qu'on partent de chez les uagers ou qu'on finisse chez eux 
    mode = models.CharField(max_length = 10, choices = [('NO_START','Vers l établissement'),('NO_END','Depuis l établissement'),('CLOSED','Vers et depuis l établissement (boucle)')], default = 'NO_START')
    # Etat de la résolution
    status = models.CharField(max_length = 10, choices = [('PENDING','Pending'),('SUCCESS','Success'),('FAILURE','Failure')], default = 'PENDING')
    # Résultat au format JSON, permet par la suite de génerer un excel, afficher une carte ect...
    result_json = models.JSONField(null = True, blank = True)
    # Date de création
    created_at = models.DateTimeField(auto_now_add = True)
    # Dernière update (en théorie au moment ou le statut devient SUCCES ou FAILURE)
    updated_at = models.DateTimeField(auto_now = True)

    # Fonction définissant l'affichage d'un objet de type Run
    def __str__(self):
        return f"Run #{self.id} - {self.groupe.nom} [{self.status}]"


