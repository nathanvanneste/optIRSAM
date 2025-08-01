from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.donnees_list, name = 'donnees_list'),
    path('infos/<str:objet_type>/<int:objet_id>/', views.infos, name = 'infos'),
    path('ajout_enfant/', views.enfant_add, name = 'add_enfant'),
]