# coding: utf-8

# from quokka.core.models import Channel, Config, CustomValue
from flask import request
from quokka.modules.analytics import record_page_view


def configure(app):
    @app.before_first_request
    def initialize():
        app.logger.info("Called only once, when the first request comes in")

    @app.before_request
    def record_view():
        record_page_view()
        
