from flask import request

from .models import PageView, IPAddress


def record_page_view():
    if (not '_theme' in request.path) and (not 'debug' in request.path):
        view = PageView(ip=dict(address=request.environ.get('X-Real-IP',False) or request.remote_addr or '000.000.000'), path=request.path)
        view.save()
