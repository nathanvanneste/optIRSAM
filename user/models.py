from django.db import models

class Adresse(models.Model):
    num_et_rue = models.CharField(max_length = 200)
    ville =  models.CharField(max_length = 50)
    code_postal = models.CharField(max_length = 20) 
    latitude  = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Numéro de voie et libellé: {self.num_et_rue}; Ville: {self.ville}; Code Postal: {self.code_postal}; Latitude: {self.latitude}; Longitude: {self.longitude}"
    
    class Meta:
        ordering = ['ville', 'code_postal']

class Etablissement(models.Model):
    nom = models.CharField(max_length = 50)
    code = models.CharField(max_length = 10)
    adresse = models.ForeignKey(Adresse, on_delete = models.SET_NULL, related_name= 'etablissements')

    def __str__(self):
        return f"Nom de l'établissement: {self.nom}; Code de l'établissement: {self.code}; Adresse: ({self.adresse})"
    
    class Meta:
        ordering = ['nom']


class Enfant(models.Model):
    prenom = models.CharField(max_length = 50)
    nom = models.CharField(max_length = 50)
    adresse = models.ForeignKey(Adresse, on_delete = models.SET_NULL, related_name = 'enfants')
    etablissement = models.ForeignKey(Etablissement, on_delete = models.CASCADE, related_name = 'enfants')

    def __str__(self):
        return f"Prénom: {self.prenom}; Nom: {self.nom}; Adresse: ({self.adresse}); Etablissement: ({self.etablissement})"

    class Meta:
        ordering = ['nom', 'prenom']

class Groupe(models.Model):
    nom = models.CharField(max_length = 50)
    enfants = models.ManyToManyField(Enfant, related_name = 'groupes')

    def __str__(self):
        return f"Nom du groupe: {self.nom}"
    
    class Meta:
        ordering = ['nom']