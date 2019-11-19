from app import db


class Task (db.Model):
    taskNo = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    year = db.Column(db.Date)
    description = db.Column(db.String(20), index=True)
    state = db.Column(db.String(20), index=True)

    def __repr__(self):
        return self.taskNo + ' ' + self.name



