#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.db import db
from quokka.core.models.content import Content


class PostImage(db.Document):
    image = db.ImageField()
    def __unicode__(self):
        return self.image.filename

class Post(Content):
    # URL_NAMESPACE = 'quokka.modules.posts.detail'
    body = db.StringField(required=True)
    image_file = db.ReferenceField(PostImage)



