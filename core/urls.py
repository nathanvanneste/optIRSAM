from django.urls import path
from . import views

urlpatterns = [
    path('', views.lancement),
    path('accueil/', views.accueil, name = 'accueil'),
]