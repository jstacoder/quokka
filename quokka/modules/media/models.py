# coding: utf-8
import logging

from flask import url_for
from jinja2 import Markup
from flask_admin import form

from quokka.core.db import db
from quokka.core.models.channel import Channel
from quokka.core.models.content import Content
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from .controller import MediaController

logger = logging.getLogger()


class Media(MediaController, Content):

    DEFAULT_CHANNEL = "media"

    path = db.StringField()
    embed = db.StringField()
    link = db.StringField()

    meta = {
        'allow_inheritance': True
    }

    @property
    def full_path(self):
        return Markup(
            "<a target='_blank' href='{full}'>{path}</a>".format(
                full=url_for('quokka.core.media', filename=self.path),
                path=self.path
            )
        )

    @classmethod
    def get_default_channel(cls):
        default_channel = cls.DEFAULT_CHANNEL
        try:
            return Channel.objects.get(long_slug=default_channel)
        except Exception as e:
            logger.warning(str(e))
            return Channel.get_homepage()

class Image(Media):
    DEFAULT_CHANNEL = 'media/images'

    @property
    def thumb(self):
        return form.thumbgen_filename(self.path)

class CloudinaryImage(db.Document):
    DEFAULT_CHANNEL = 'media/images'

    main_image_path = db.StringField()
    thumbnail_path = db.StringField()
    avatar_path = db.StringField()
    public_id = db.StringField()
    file_name = db.StringField()

    @classmethod
    def create_new_image(cls, file_from_request):
        instance = cls()

        upload_result = upload(file_from_request)
        instance.public_id = upload_result.get('public_id')
        instance.thumbnail_path, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=100,
                                                     height=100)
        instance.avatar_path, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=100,
                                                     height=100, radius=20, effect="sepia")
        instance.main_image_path = upload_result.get('url')
        instance.file_name = upload_result.get('original_filename')
        instance.save()
        return instance

    @property
    def full_path(self):
        return Markup(
            "<a target='_blank' href='{main_image_path}'>{file_name}</a>".format(
                main_image_path=self.main_image_path,
                file_name=self.file_name
            )
        )

    @property
    def thumb(self):
        return self.thumbnail_path

    @property
    def avatar(self):
        return self.avatar_path
     

class File(Media):
    DEFAULT_CHANNEL = 'media/files'


class Video(Media):
    DEFAULT_CHANNEL = 'media/videos'


class Audio(Media):
    DEFAULT_CHANNEL = 'media/audios'


class MediaGallery(Content):
    body = db.StringField(required=False)
    media_type = db.StringField(choices=(('file','File'),('video','Video'),('audio','Audio'),('image','Image')), default=('image','Image'))
    items = db.ListField(db.ReferenceField(Image))


