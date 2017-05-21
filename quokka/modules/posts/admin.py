# coding : utf -8

from quokka import admin
from quokka.core.admin.models import BaseContentAdmin, ModelAdmin
from quokka.core.widgets import TextEditor, PrepopulatedText
from .models import Post, PostImage
from quokka.utils.translation import _l


class PostAdmin(BaseContentAdmin):
    def scaffold_list_columns(self, *args, **kwargs):        
        column_list = list(super(PostAdmin, self).scaffold_list_columns(*args, **kwargs))
        column_list += ['image_file']
        return column_list

    column_list = ('image_file',)

    column_searchable_list = ('title', 'body', 'summary')

    form_columns = ['title', 'slug', 'channel', 'related_channels', 'summary',
                    'content_format', 'body', 'authors',
                    'comments_enabled', 'published', 'add_image', 'contents',
                    'show_on_channel', 'available_at', 'available_until',
                    'tags', 'values', 'template_type', 'license', 'image_file']

    form_args = {
        'body': {'widget': TextEditor()},
        'summary': {'widget': TextEditor()},
        'slug': {'widget': PrepopulatedText(master='title')}
    }

class PostImageAdmin(ModelAdmin):
    """ """

admin.register(PostImage, PostImageAdmin, category="Content", name="images")
admin.register(Post, PostAdmin, category=_l("Content"), name=_l("Post"))
