from django import template
"""
 custom tag which will be used at  the paginator html file 
 to allow a mix paginator and filter of data
 """

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):

    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()