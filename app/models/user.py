from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    inspections = db.relationship('Inspection', backref='inspector', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"