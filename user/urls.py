from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.donnees_list, name = 'donnees_list'),
    path('infos/<str:objet_type>/<int:objet_id>/', views.infos, name = 'infos'),
    path('ajout_enfant/', views.enfant_add, name = 'add_enfant'),
    path('ajout_groupe/', views.groupe_add, name = 'add_groupe'),
    path('modifier_enfant/<int:enfant_id>/', views.enfant_edit, name = 'edit_enfant'),
    path('modifier_groupe/<int:groupe_id>/', views.groupe_edit, name = 'edit_groupe'),
    path('supprimer_enfant/<int:enfant_id>/', views.enfant_remove, name = 'remove_enfant'),
    path('supprimer_groupe/<int:groupe_id>/', views.groupe_remove, name = 'remove_groupe'),
    path('dupliquer_enfant/<int:enfant_id>/', views.enfant_duplicate, name = 'duplicate_enfant'),
]