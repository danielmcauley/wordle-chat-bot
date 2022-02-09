from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_str=db.Column(db.String(32), unique=True)
    answer=db.Column(db.String(32))
    tries=db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.from_str

    def __init__(self, from_str, answer): #, **kwargs):
        # super(User, self).__init__(**kwargs)
        self.from_str=from_str
        self.answer=answer
        self.tries = 0

    def __repr__(self):
        return '<User %r>' % self.from_str
