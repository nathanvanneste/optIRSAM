from django.db import models

class Adresse(models.Model):
    num_et_rue = models.CharField(max_length = 200)
    ville =  models.CharField(max_length = 50)
    code_postal = models.CharField(max_length = 20) 
    latitude  = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.num_et_rue}, {self.ville}"
    
    class Meta:
        ordering = ['ville', 'code_postal']

class Etablissement(models.Model):
    nom = models.CharField(max_length = 50)
    code = models.CharField(max_length = 10)
    adresse = models.ForeignKey(Adresse, on_delete = models.SET_NULL, null = True, blank = True, related_name= 'etablissements')

    def __str__(self):
        return f"{self.nom}"
    
    class Meta:
        ordering = ['nom']


class Enfant(models.Model):
    prenom = models.CharField(max_length = 50)
    nom = models.CharField(max_length = 50)
    adresse = models.ForeignKey(Adresse, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'enfants')
    etablissement = models.ForeignKey(Etablissement, on_delete = models.CASCADE, related_name = 'enfants')

    def __str__(self):
        return f"{self.nom}, {self.prenom}"

    class Meta:
        ordering = ['nom', 'prenom']

class Groupe(models.Model):
    nom = models.CharField(max_length = 50)
    enfants = models.ManyToManyField(Enfant, related_name = 'groupes')

    def __str__(self):
        return f"{self.nom}"
    
    class Meta:
        ordering = ['nom']