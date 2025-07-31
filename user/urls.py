from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.donnees_list),
    path('add/', EnfantCreate.as_view(), name = 'enfant_add'),
    path('<int:pk>/edit/', EnfantUpdate.as_view(), name = 'enfant_edit'),
    path('<int:pk>/delete', EnfantDelete.as_view(), name = 'enfant_delete'),

    path('groupes/', GroupeList.as_view(), name = 'groupe_list'),
    path('groupes/add/', GroupeCreate.as_view(), name = 'groupe_add'),
    path('groupes/<int:pk>/edit/', GroupeUpdate.as_view(), name = 'groupe_edit'),
    path('groupes/<int:pk>/delete/', GroupeDelete.as_view(), name = 'groupe_delete'),
]