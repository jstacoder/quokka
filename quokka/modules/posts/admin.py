# coding : utf -8
import pickle

from flask import request, Response
from jinja2 import Markup

from redis.exceptions import ResponseError

from quokka import admin
from quokka.core.admin.models import BaseContentAdmin, ModelAdmin
from quokka.core.widgets import TextEditor, PrepopulatedText
from quokka.utils.routing import expose
from quokka.core.config import load_redis
from .models import Post, PostImage
from quokka.utils.translation import _l
from flask_admin.contrib.mongoengine.view import ModelView
from quokka.modules.media.models import CloudinaryImage

from flask_wtf import FlaskForm as Form
from wtforms import fields, widgets, validators

import logging
logger = logging.getLogger()


class UploadForm(Form):
    file = fields.FileField('file upload')
    name = fields.StringField()    

def _list_thumbnail_cloudinary(instance, context, model, name):
    #if not hasattr(model,'thumbnail_path'):
    #    model = getattr(model,'image_file')
    thumbnail = ''
    if hasattr(model, 'thumbnail_path'):
        if not model.thumbnail_path:
            return ''
        thumbnail = model.thumbnail_path
    else:
        if hasattr(model,'image_file'):
            if not model.image_file:
                return ''
            thumbnail = model.image_file.thumbnail_path
    return Markup(
        '<img src="{}" width=100>'.format(thumbnail)
    )

class CloudinaryAdmin(ModelView):
    column_formatters = {
        'thumb': _list_thumbnail_cloudinary
    }

    def edit_form(self, obj=None):
        class FormClass(object):
            file = None
            name = None

        fc = FormClass()
        if obj:
            fc.file = obj.main_image_path
            fc.name = obj.file_name
        return super(CloudinaryAdmin, self).edit_form(obj=fc)
        

    def get_form(self):
        return UploadForm

    def create_model(self, form):        
        file_names = request.files.keys()
        file_obj = request.files.get(file_names[0])        
        file_obj.name = file_obj.filename if form.name.data is None else form.name.data
        try:
            model = self.model.create_new_image(file_obj)
            self._on_model_change(form, model, True)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s',
                              error=format_error(ex)),
                      'error')
                logger.exception('Failed to create record.')

            return False
        else:
            self.after_model_change(form, model, True)

        return model


    list_columns = ('main_image_path','thumb','public_id','file_name',)

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
    column_formatters = {
        'image_file': _list_thumbnail_cloudinary
    }

class PostImageAdmin(ModelView):
    column_list = ('name', 'filetype', 'image',)
    form_columns = ('name','image',)
    column_editable_list = ('name',)

    @expose('/api/file/')
    def api_file_view(self):
        image = None
        redis = load_redis()
        pk = request.args.get('id')    
        if pk in redis.keys("*"):
            image = pickle.loads(redis.get(pk))                    
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
                pass
        return response 
        
        def is_accessible(self):
            return True

        def _handle_view(self, *args, **kwargs):
            pass

admin.register(PostImage, PostImageAdmin, category="Content", name="images")
admin.register(Post, PostAdmin, category=_l("Content"), name=_l("Post"))
admin.register(CloudinaryImage, CloudinaryAdmin, category="Content", name="new")