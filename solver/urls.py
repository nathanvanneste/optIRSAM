from django.urls import path
from . import views

urlpatterns = [
    path('', views.run_create),
    path("run/<int:pk>/", views.run_detail, name="run_detail"),
    path('download/<int:pk>/', views.download_excel, name='download_excel'),
]