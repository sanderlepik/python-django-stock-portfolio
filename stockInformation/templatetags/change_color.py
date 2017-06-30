from django import template


register = template.Library()


@register.filter
def change_color(value):
    if value > 0:
        return "#093"
    elif value <= 0:
        return "#d14836"
