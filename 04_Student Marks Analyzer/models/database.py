from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True )
    filename = db.Column(db.String(255),nullable = False)
    upload_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"<Upload {self.filename}>"