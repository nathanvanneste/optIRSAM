from django.db import models

# Ensemble des modèles de l'application user 

# Moèle Adresse 
class Adresse(models.Model):
    # Numéro et libéllé de voie 
    num_et_rue = models.CharField()
    # Ville 
    ville =  models.CharField(max_length = 254)
    # Code postal 
    code_postal = models.CharField(max_length = 20) 
    # Grâce aux trois champs supérieurs on peut récupèrer les coordonnées grâce à une API OSRM. Ces dernières sont indispensables pour définir les matrices de coût dans la résolution
    latitude  = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.num_et_rue}, {self.ville}"
    
    class Meta:
        ordering = ['ville', 'code_postal']

# Modèle Etablissement 
class Etablissement(models.Model):
    # Nom de l'établissement 
    nom = models.CharField(max_length = 50)
    # Code de l'établissement => pas d'utilité actuelle mais peut ouvrir sur des usages futurs 
    code = models.CharField(max_length = 30)
    # Adresse de l'établissement
    adresse = models.ForeignKey(Adresse, on_delete = models.SET_NULL, null = True, blank = True, related_name= 'etablissements')

    def __str__(self):
        return f"{self.nom}"
    
    class Meta:
        ordering = ['nom']

# Modèle enfant
class Enfant(models.Model):
    # Prenom de l'enfant
    prenom = models.CharField(max_length = 254)
    # Nom de l'enfant 
    nom = models.CharField(max_length = 254)
    # Utile pour parents séparés, comme il y a plusieurs adresses => permet de créer plusieurs instances d'un même enfant
    tuteur = models.CharField(max_length = 100, default = 'Parents')
    # Adresse de l'enfant
    adresse = models.ForeignKey(Adresse, on_delete = models.SET_NULL, null = True, blank = True, related_name = 'enfants')
    # Etablissement de l'enfant 
    etablissement = models.ForeignKey(Etablissement, on_delete = models.CASCADE, related_name = 'enfants')

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.tuteur})"

    class Meta:
        ordering = ['nom', 'prenom']

# Modèle Groupe => liste d'enfants avec un établissement associé => permet de regrouper les enfants d'une résolution 
class Groupe(models.Model):
    # Nom du groupe. Exemple : Tournée du lundi IRS...
    nom = models.CharField(max_length = 50)
    # Liste d'objets Enfant faisant partis d'un même groupe donc d'une même résolution 
    enfants = models.ManyToManyField(Enfant, related_name = 'groupes')
    # Etablissement des enfants du groupe (mis en attribut pour faciliter la résolution)
    etablissement = models.ForeignKey(Etablissement, on_delete = models.CASCADE, related_name = 'groupes')

    def __str__(self):
        return f"{self.nom}"
    
    class Meta:
        ordering = ['nom']