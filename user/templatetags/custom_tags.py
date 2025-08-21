from django import template
from user.models import Enfant

# Permet de récuperer un etablissement à partir de l'id d'un enfant, ce qui est beaucoup plus simple de le faire là plutôt que dans le template où on 
# a pas un objet enfant directement mais juste un id => necessité donc de passer par un guetteur

register = template.Library()

@register.filter
def get_etab_id(enfant_id):
    if not enfant_id:
        return None
    try:
        value = getattr(enfant_id, 'pk', None) or getattr(enfant_id, 'value', None) or enfant_id
        enfant_id_int = int(value)
        enfant = Enfant.objects.get(id=enfant_id_int)
        return enfant.etablissement.id if enfant.etablissement else None
    except (ValueError, Enfant.DoesNotExist, TypeError):
        return None

