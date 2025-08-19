from django.urls import path
from . import views

urlpatterns = [
    path('', views.run_create, name = 'parametrage'),
    path("run/<int:pk>/", views.run_detail, name='run_detail'),
    path('download/<int:pk>/', views.download_excel, name='download_excel'),
    path("runs/", views.run_list, name="run_list"),
]