from jinja2 import Template

def render_template(string, context):
    template = Template(string)
    return template.render(context)
