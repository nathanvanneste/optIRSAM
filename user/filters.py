import django_filters
from .models import Enfant, Etablissement

class EnfantFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(lookup_expr='icontains', label="Nom")
    prenom = django_filters.CharFilter(lookup_expr='icontains', label="Prénom")
    etablissement = django_filters.ModelChoiceFilter(queryset=Etablissement.objects.all())

    class Meta:
        model = Enfant
        fields = ['nom', 'prenom', 'etablissement']
