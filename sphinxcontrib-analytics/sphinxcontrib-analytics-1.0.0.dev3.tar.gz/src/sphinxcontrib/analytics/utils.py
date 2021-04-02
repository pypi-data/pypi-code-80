from jinja2 import Environment, PackageLoader, select_autoescape


def render_template(template_name, context):
    env = Environment(
        loader=PackageLoader(__package__, '_templates'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template(template_name)
    return template.render(context)
