# coding : utf -8
from wtforms.fields import TextField
from wtforms.widgets import PasswordInput
from quokka import admin
from quokka.core.admin.models import ModelAdmin
from quokka.utils.translation import _l

from .models import Role, User, Connection#, ContactInfo
#from .forms import CreateContactInfoForm

'''class ContactInfoAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('user.username', 'user.name', 'user.email')

    def get_column_name(self, col):
        return col.split('.')[-1].title()

    def get_edit_form(self, *args, **kwargs):
        return CreateContactInfoForm
'''
class UserAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_searchable_list = ('name', 'email')
    column_list = ('name', 'email', 'active',
                   'last_login_at', 'login_count')
    form_columns = ('name', 'email', 'roles', 'active', 'newpassword',
                    'confirmed_at',
                    'last_login_at', 'current_login_at', 'last_login_ip',
                    'current_login_ip', 'login_count', 'tagline',
                    'gravatar_email', 'use_avatar_from',
                    'avatar_file_path', 'avatar_url',
                    'bio', 'links', 'values')

    form_extra_fields = {
        "newpassword": TextField(widget=PasswordInput())
    }

    def on_model_change(self, form, model, is_created):
        if model.newpassword:
            setpwd = model.newpassword
            del model.newpassword
            model.set_password(setpwd, save=True)
        


class RoleAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('name', 'description', 'values')


class ConnectionAdmin(ModelAdmin):
    roles_accepted = ('admin',)


admin.register(User, UserAdmin, category=_l("Accounts"), name=_l("User"))
admin.register(Role, RoleAdmin, category=_l("Accounts"), name=_l("Roles"))
admin.register(Connection, ConnectionAdmin,
               category=_l("Accounts"), name=_l("Connection"))
#admin.register(ContactInfo, ContactInfoAdmin, category=_l('Accounts'), name=_l('Contact Info'))