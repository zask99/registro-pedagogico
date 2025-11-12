# mi_admin/templatetags/custom_filters.py
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retrieves an item from a dictionary using a given key.
    Useful for accessing dictionary values dynamically in Django templates.
    """
    return dictionary.get(key)

@register.filter
def get_rango_clase(nota_final):
    """
    Devuelve la clase CSS para el rango de la nota.
    """
    if nota_final is None:
        return ""
    
    nota_final = Decimal(str(nota_final)) # Asegurar que es Decimal para comparación

    if 0 <= nota_final <= 59:
        return "nota-final-ed"  # En Desarrollo
    elif 60 <= nota_final <= 69:
        return "nota-final-da"  # Desarrollo Adecuado
    elif 70 <= nota_final <= 89:
        return "nota-final-do"  # Desarrollo Óptimo
    elif 90 <= nota_final <= 100:
        return "nota-final-dp"  # Desarrollo Pleno
    else:
        return "" # O una clase por defecto si la nota está fuera de rango

@register.filter(name='split')
def split(value, arg):
    """
    Splits a string by the given argument.
    Example: {{ value|split:"," }}
    """
    return value.split(arg)