# -*- coding: utf-8 -*-
import os

from quokka.core.db import db
from quokka.core.models.content import Content
from quokka.modules.media.models import CloudinaryImage


class PostImage(db.Document):
    image = db.ImageField()
    name = db.StringField(default='', max_length=255)
    filetype = db.StringField(choices=['jpg','png','bmp'], default='jpg')

    def __init__(self, *args, **kwargs):
        super(PostImage, self).__init__(*args, **kwargs)
        if not self.name:
            self.name, self.filetype = os.path.splitext(self.image.filename)

    def __unicode__(self):
        return self.image.filename

class Post(Content):
    # URL_NAMESPACE = 'quokka.modules.posts.detail'
    body = db.StringField(required=True)
    image_file = db.ReferenceField(CloudinaryImage)



