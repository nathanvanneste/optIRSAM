from django import template
from user.models import Enfant

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

