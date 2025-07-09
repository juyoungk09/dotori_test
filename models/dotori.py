from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db import db

class UserDotori(db.Model):
    __tablename__ = 'user_dotori'
    
    id = db.Column(db.Integer, primary_key=True)
    dotori_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'user_id': self.id,
            'dotori_count': self.dotori_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def to_response(self):
        return {
            'userId': self.id,
            'dotory': self.dotori_count
        }

    def increment(self, amount=1):
        self.dotori_count += amount
        self.updated_at = datetime.now()
        return self.dotori_count

    def decrement(self, amount=1):
        if self.dotori_count >= amount:
            self.dotori_count -= amount
            self.updated_at = datetime.now()
            return self.dotori_count
        return False
    def __repr__(self):
        return f"<UserDotori user_id={self.id} dotori_count={self.dotori_count}>"