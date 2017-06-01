#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect, url_for
from flask.views import MethodView
from quokka.core.templates import render_template

from ..mixins.views import TemplateMixin
from ..mixins.forms import FormMixin

from flask_wtf import FlaskForm as Form
from wtforms import fields, widgets, validators

from .models import Media, CloudinaryImage

import logging
logger = logging.getLogger()


class UploadForm(Form):
    file = fields.FileField('file upload')
    submit = fields.SubmitField('submit')

class ListCloudinaryView(FormMixin, TemplateMixin):
    template_name = 'media/list.html'
    form_class = UploadForm
    
    def get(self):
        logger.info('getting media from cloudinary')        
        return super(ListCloudinaryView, self).get()

    def post(self):
        upload_file = self.request.files['file']
        CloudinaryImage.create_new_image(upload_file)
        return redirect(url_for('.list_cloud'))


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
