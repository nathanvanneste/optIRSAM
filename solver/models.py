from django.db import models
from user.models import Groupe, Etablissement

class Run(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete = models.CASCADE, related_name = 'runs')
    etablissement = models.ForeignKey(Etablissement, on_delete = models.CASCADE, related_name = 'runs')
    capacity = models.PositiveIntegerField()
    time_limit = models.PositiveIntegerField(help_text = "en secondes")
    calculation_mod = models.CharField(max_length = 10, choices = [('DISTANCE','Distance'),('DURATION','Duration')], default = 'DISTANCE')
    status = models.CharField(max_length = 10, choices = [('PENDING','Pending'),('SUCCESS','Success'),('FAIL','Fail')], default = 'PENDING')
    result_json = models.JSONField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"Run #{self.id} - {self.groupe.nom} [{self.status}]"


