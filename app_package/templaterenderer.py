from jinja2 import Environment, Markup, PackageLoader, select_autoescape


class TemplateRenderer:
    def __init__(self):
        self.env = Environment(
            loader=PackageLoader('app_package', '../templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render(self, template_file, **kwargs):
        template = self.env.get_template(template_file)
        return template.render(kwargs)
