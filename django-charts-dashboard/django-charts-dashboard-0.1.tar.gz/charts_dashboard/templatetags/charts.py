from django import template

register = template.Library()


@register.inclusion_tag("charts_dashboard/chart.html", takes_context=True)
def render_chart(context, values):
    return {
        "chart": values,
        "tooltips": list(*context["tooltips"]),
        "height": context.get("height"),
        "width": context.get("width"),
    }
