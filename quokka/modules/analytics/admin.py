from quokka.core.admin.models import ModelAdmin
from .models import PageView
from quokka import admin

class PageViewAdmin(ModelAdmin):
    can_edit = False
    can_delete = True
    can_add = False

    list_columns = ('time', 'ip.address','path')

admin.register(PageView, PageViewAdmin, name='page views', category='analytics')