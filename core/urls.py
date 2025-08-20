from django.urls import path
from . import views

# Redirection lors d'accès via une URL vide
urlpatterns = [
    path('', views.lancement),
    path('accueil/', views.accueil, name = 'accueil'),
]