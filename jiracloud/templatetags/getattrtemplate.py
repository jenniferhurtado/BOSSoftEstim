from django import template
register = template.Library()


@register.filter
def getattrtemplate(obj, args):
    """ Try to get an attribute from an object.

    Example: {% if block|getattr:"editable,True" %}

    Beware that the default is always a string, if you want this
    to return False, pass an empty second argument:
    {% if block|getattr:"editable," %}
    """
    default = ''
    attribute = args
    try:
        return obj.__getattribute__(attribute)

    except AttributeError:
         return obj.__dict__.get(attribute, default)

    except:
        return default
