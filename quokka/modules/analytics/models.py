from datetime import datetime
from quokka.core.db import db

class IPAddress(db.EmbeddedDocument):
    address = db.StringField(max_length=255, required=True)

class PageView(db.Document):
    time = db.DateTimeField(default=datetime.now)
    ip = db.EmbeddedDocumentField(IPAddress)
    path = db.StringField(max_length=255)


    

