from django.contrib import admin
from .models import Adresse, Etablissement, Enfant, Groupe

admin.site.register(Adresse)
admin.site.register(Etablissement)
admin.site.register(Enfant)
admin.site.register(Groupe)
