# coding : utf -8
import pickle

from flask import request, Response

from redis.exceptions import ResponseError

from quokka import admin
from quokka.core.admin.models import BaseContentAdmin, ModelAdmin
from quokka.core.widgets import TextEditor, PrepopulatedText
from quokka.utils.routing import expose
from quokka.core.config import load_redis
from .models import Post, PostImage
from quokka.utils.translation import _l


class PostAdmin(BaseContentAdmin):
    def scaffold_list_columns(self, *args, **kwargs):        
        column_list = list(super(PostAdmin, self).scaffold_list_columns(*args, **kwargs))
        column_list += ['image_file']
        return column_list

    column_list = ('title', 'channel', 'published', 'image_file',)

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
    column_list = ('name', 'filetype',)
    form_columns = ('name','image',)

    @expose('/api/file/')
    def api_file_view(self):
        image = None
        redis = load_redis()
        pk = request.args.get('id')    
        if pk in redis.keys("*"):
            image = pickle.loads(redis.get(pk))            
        if 'keys_{}'.format(pk) in redis.keys("*"):
            key1, key2 = redis.get('keys_{}'.format(pk)).split(':')
            part1 = pickle.loads(redis.get(key1))
            part2 = pickle.loads(redis.get(key2))
            image = part1 + part2
        if image is not None:
            response = Response(image,
                        content_type="image/jpeg",
                        headers={
                            'Content-Length': len(image)
                        }
            )
            return response
        else:
            response = super(PostImageAdmin, self).api_file_view()
            image = response.data
            try:
                redis.set(pk, pickle.dumps(image), ex=5000)
            except ResponseError:
                keys_key = 'keys_{}'.format(pk)
                keys = 'key1_{0}:key2_{0}'.format(pk)
                redis.set(keys_key, keys)
                size = len(image)
                first_half = image[:size/2]
                last_half = image[size/2:]
                redis.set('key1_{}'.format(pk), pickle.dumps(first_half))
                redis.set('key2_{}'.format(pk), pickle.dumps(last_half))
        return response 


admin.register(PostImage, PostImageAdmin, category="Content", name="images")
admin.register(Post, PostAdmin, category=_l("Content"), name=_l("Post"))
