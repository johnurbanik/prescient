from app import db
from sqlalchemy.sql import func


class KV(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<KV {}: {}>'.format(self.key, self.value)


class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Integer, unique=False, nullable=False, index=True)
    value = db.Column(db.Integer, unique=False, nullable=False, index=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False, index=True)
    time = db.Column(db.DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return '<Key {} was accessed by {} at {}'.format(self.key, self.user_id, self.time)
