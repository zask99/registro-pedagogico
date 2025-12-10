from django import template
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.models import QuerySet # Importación corregida
from django.db import models  # Esta linha é crucial para o Pylance

register = template.Library()
class EnhancedDjangoJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder que puede serializar objetos de modelos de Django
    de una manera controlada para evitar referencias circulares.
    """
    def default(self, o):
        # Maneja QuerySets
        if isinstance(o, QuerySet):
            return list(o.values())  # Convertir a lista de diccionarios para evitar el problema

        # Maneja objetos de modelos de Django
        if isinstance(o, models.Model):
            # Obtiene los datos del modelo como un diccionario
            data = {}
            for field in o._meta.fields:
                value = getattr(o, field.name)
                # Serializa valores de clave externa a solo su ID para evitar la recursión
                if isinstance(value, models.Model):
                    data[field.name] = value.id
                else:
                    data[field.name] = value

            # Maneja relaciones OneToOne, como 'persona'
            if hasattr(o, 'persona'):
                # En lugar de serializar el objeto persona completo,
                # extraemos solo los campos que necesitamos.
                persona_data = {
                    'id': o.persona.id,
                    'nombres': o.persona.nombres,
                    'apellidos': o.persona.apellidos
                }
                data['persona'] = persona_data
            
            return data

        # Permite que el codificador base maneje otros tipos de datos
        return super().default(o)

@register.filter(name='to_json')
def to_json(value):
    """
    Serializa un valor a una cadena JSON, manejando objetos de Django.
    """
    if isinstance(value, str):
        return value
    return json.dumps(value, cls=EnhancedDjangoJSONEncoder)


@register.filter
def get_item(dictionary, key):
    """
    Retrieves an item from a dictionary using a given key.
    Useful for accessing dictionary values dynamically in Django templates.
    """
    return dictionary.get(key)