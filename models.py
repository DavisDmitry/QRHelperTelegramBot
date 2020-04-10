from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    language = db.Column(db.String(2), nullable=True)
    string = db.Column(db.String(4096))
    scale = db.Column(db.Integer)
    qz = db.Column(db.Integer)
    color = db.Column(db.String(11))
    bg = db.Column(db.String(11))