#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.db import db
from quokka.core.models.content import Content


class PostImage(db.DynamicDocument):
    image = db.ImageField()

class Post(Content):
    # URL_NAMESPACE = 'quokka.modules.posts.detail'
    body = db.StringField(required=True)
    image_file = db.RefereceField(PostImage)
        
