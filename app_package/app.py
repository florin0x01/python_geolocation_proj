from .templaterenderer import TemplateRenderer


class App:
    def __init__(self):
        self.renderer = TemplateRenderer()

    def list_stores(self, stores):
        return self.renderer.render('template1.html', stores=stores)

    def display_stores(self):
        return self.renderer.render('search_tmpl.html')