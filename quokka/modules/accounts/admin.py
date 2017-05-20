# coding : utf -8
from wtforms.fields import TextField
from wtforms.widgets import PasswordInput
from quokka import admin
from quokka.core.admin.models import ModelAdmin
from quokka.utils.translation import _l
from flask_admin.form import rules
from flask_admin.contrib.mongoengine.fields import MongoImageField
from IPython import embed
from flask_mongoengine.fields import ImageField

from ...core.admin.fields import MyContentImageField
from .models import Role, User, Connection, UserProfile, TestImage
#from .forms import CreateContactInfoForm

'''class ContactInfoAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_list = ('user.username', 'user.name', 'user.email')

    def get_column_name(self, col):
        return col.split('.')[-1].title()

    def get_edit_form(self, *args, **kwargs):
        return CreateContactInfoForm
'''

class DBImageAdmin(ModelAdmin):
    """ """
    def on_model_change(self, form, instance, created):
        if not instance.title:
            instance.title = self._make_image_title(instance)
            instance.save()

    def _make_image_title(self, image):
        if not image.image.filename:
            return ''
        return os.path.splitext(image.image.filename)[0].lower()
        

'''class UserProfileAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    form_create_rules = [
        rules.FieldSet(('username','email'), 'User Data'),
        rules.Header("TESTING!!!"),
        rules.Field("email"),
        "username",
        rules.Text(
            "<h2>Hmmmmm</h2>"
        ),
        rules.Container("_testing.test", rules.Field("email"))
    ]

    embed()
'''
class UserAdmin(ModelAdmin):
    roles_accepted = ('admin',)
    column_searchable_list = ('name', 'email')
    column_list = ('name', 'email', 'active',
                   'last_login_at', 'login_count',
                   'current_login_ip','last_login_ip', 'images')
    form_columns = ('name', 'email', 'roles', 'active', 'newpassword',
                    'confirmed_at','tagline','gravatar_email', 'use_avatar_from',
                    'avatar_file_path', 'avatar_url',
                    'bio', 'links', 'values', 'images')

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
admin.register(DBImage, DBImageAdmin, name="DB Images")
#admin.register(UserProfile, UserProfileAdmin, category=_l("Accounts"),name=_l("User Profiles"))
#admin.register(TestImage, TestAdmin, category=_l('Test'),name=_l('Test'))
#admin.register(ContactInfo, ContactInfoAdmin, category=_l('Accounts'), name=_l('Contact Info'))