from flask import views, request, current_app
from quokka.core.templates import render_template

class BaseView(views.MethodView): 
    @property
    def request(self):
        return request

    @property
    def app(self):
        return current_app

    def get(self, *args, **kwargs):
        return self.render(*args, **kwargs)

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)    
    

class ContextMixin(BaseView):    
    def get_context_data(self, **kwargs):
        context = kwargs
        return context

    def render(self, *args, **kwargs):
        context = self.get_context_data()
        kwargs.update(context)
        return super(ContextMixin, self).render(*args, **kwargs)


class TemplateMixin(BaseView):
    template_name = None

    def get_template_name(self):
        if self.template_name is None:
            raise ValueError("{} needs a template".format(self.__class__.__name__))
        return self.template_name

    def render(self, *args, **kwargs):
        return super(TemplateMixin, self).render(self.get_template_name(), *args, **kwargs)

    