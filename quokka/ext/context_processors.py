# coding: utf-8
import os
import datetime
from quokka.core.models.channel import Channel
from quokka.core.models.config import Config
from quokka.core.models.content import Content, Link
from flask_admin.helpers import get_url
from flask import request
from functools import partial

load_req_val = lambda name: getattr(request, name)
load_req_path = partial(load_req_val,'path')
load_req_endpoint = partial(load_req_val, 'endpoint')


def get_current_theme_path(app):
    add_to_path = None
    current_theme_name, theme_type, trash = load_req_endpoint().split('.')[0].rsplit('_',2)
    current_path = load_req_path().split('/b/')
    if len(current_path) > 1:
        add_to_path = current_path[-1]
    try:
        current_theme = filter(lambda b: b == current_theme_name, app.theme_manager.themes)[0]
        path_args = [app.theme_manager.themes[current_theme].path, theme_type]
        if add_to_path is not None:
            path_args.append(add_to_path)
        return os.path.join(*path_args)
    except:
        return current_theme_name, theme_type, current_path
def configure(app):
    load_theme_path = lambda: get_current_theme_path(app)

    @app.context_processor
    def inject():
        now = datetime.datetime.now()
        return dict(
            channels=Channel.objects(published=True,
                                     available_at__lte=now,
                                     parent=None),
            Config=Config,
            Content=Content,
            Channel=Channel,
            homepage=Channel.get_homepage(),
            Link=Link,
            dir=dir,
	    get_url=get_url,
            request_path=load_req_path,
            request_endpoint=load_req_endpoint,
            bp=map(str,app.blueprints),
	    theme_path=load_theme_path, 
        )
