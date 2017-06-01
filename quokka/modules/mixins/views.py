from flask import views

class ContextMixin(BaseView):    
    def get_context_data(self, **kwargs)
        context = kwargs
        return context

class TemplateMixin(BaseView):
    template_name = None

    def get_template_name(self):
        if self.template_name is None:
            raise ValueError("{} needs a template".format(self.__class__.__name__))
        return self.template_name

    