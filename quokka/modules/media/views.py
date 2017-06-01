#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.views import MethodView
from quokka.core.templates import render_template

from quokka.modules.mixins.views import ContextMixin, TemplateMixin

from .models import Media, CloudinaryImage

import logging
logger = logging.getLogger()


class ListCloudinaryView(ContextMixin, TemplateMixin):
    template_name = 'media/list.html'
    
    def get(self):
        logger.info('getting media from cloudinary')        
        return super(ListCloudinaryView, self).get()



class ListView(MethodView):

    def get(self):
        logger.info('getting list of media')
        medias = Media.objects.all()
        return render_template('media/list.html', medias=medias)


class DetailView(MethodView):

    @staticmethod
    def get_context(slug):
        media = Media.objects.get_or_404(slug=slug)

        context = {
            "media": media
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('medias/detail.html', **context)
