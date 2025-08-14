from django.db import models
from user.models import Groupe, Etablissement

class Run(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete = models.CASCADE, related_name = 'runs')
    etablissement = models.ForeignKey(Etablissement, on_delete = models.CASCADE, related_name = 'runs', null=True, blank=True)
    vehicules = models.CharField(max_length = 50, choices = [('VOITURES','Voitures (5 places)'),('VANS','Vans (9 places)'),('VOITURES_ET_VANS','Voitures et vans')], default = 'VOITURES')
    time_limit = models.PositiveIntegerField(help_text = "en secondes")
    calculation_mod = models.CharField(max_length = 10, choices = [('DISTANCE','Distance'),('DURATION','Durée')], default = 'DISTANCE')
    mode = models.CharField(max_length = 10, choices = [('NO_START','Vers le dépôt'),('NO_END','Depuis le depôt'),('CLOSED','Vers et depuis le dépôt (boucle)')], default = 'CLOSED')
    status = models.CharField(max_length = 10, choices = [('PENDING','Pending'),('SUCCESS','Success'),('FAILURE','Failure')], default = 'PENDING')
    result_json = models.JSONField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Run #{self.id} - {self.groupe.nom} [{self.status}]"


