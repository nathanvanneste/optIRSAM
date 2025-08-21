from django.contrib import admin
from .models import Adresse, Etablissement, Enfant, Groupe

# Enregistrement des modeles pour pouvoir les gérer sur url_de_base/admin 

admin.site.register(Adresse)
admin.site.register(Etablissement)
admin.site.register(Enfant)
admin.site.register(Groupe)
