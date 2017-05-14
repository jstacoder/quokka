# coding : utf -8


from quokka import admin
from quokka.core.admin.models import ModelAdmin
from quokka.core.widgets import TextEditor
from .models import Comment
from quokka.utils.translation import _l
from wtforms import widgets



from flask_admin.contrib.mongoengine.filters import BaseMongoEngineFilter

class ViewedByModeratorFilter(BaseMongoEngineFilter):
    filter_options = (('1', 'Yes'), ('0', 'No'))

    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', None)
        if options is None:
            options = self.filter_options
        kwargs['options'] = options
        super(ViewedByModeratorFilter, self).__init__(*args, **kwargs)

    def apply(self, query, value):
        if value == '1':
            return query.filter(viewed_by_moderator=True)
        else:
            return query.filter(viewed_by_moderator__ne=True)

    def operation(self):
        return 'Was viewed by moderator'

class CommentAdmin(ModelAdmin):
    roles_accepted = ('admin', 'editor', 'moderator')
    column_list = ('path', 'author_name', 'author_email',
                   'created_at', 'published', 'viewed_by_moderator')
    form_columns = ['path', 'author_email', 'author_name',
                    'content_format', 'body', 'replies',
                    'created_at', 'created_by', 'published', 'viewed_by_moderator']
    form_args = {
        'body': {'widget': TextEditor()},
        'viewed_by_moderator': {'widget': widgets.HiddenInput() }
    }
    column_filters = [
        ViewedByModeratorFilter(
            column=Comment.viewed_by_moderator,
            name='viewed by moderator',            
    )]

    def get_one(self, _id):
        rtn = super(CommentAdmin, self).get_one(_id)
        if not rtn.viewed_by_moderator:
            rtn.viewed_by_moderator = True
            rtn.save()
        return rtn

admin.register(Comment, CommentAdmin, category=_l('Content'),
               name=_l("Comments"))
