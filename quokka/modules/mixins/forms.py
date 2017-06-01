
class FormMixin(object):
    form_class = None

    def get_form_class(self):
        if self.form_class is None:
            raise ValueError("needs a form class")
        return self.form_class

    def get_context_data(self, **kwargs):
        context = super(ViewName, self).get_context_data(**kwargs)
        context['form'] = self.get_form_class()()
        return context