from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

favorite_character = db.Table(
    'favorite_character',    
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id'), nullable=False, primary_key=True)
)

favorite_planet = db.Table(
    'favorite_planet',     
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), nullable=False, primary_key=True)    
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120),  nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    planets = db.relationship('Planet', secondary='favorite_planet')
    characters = db.relationship('Character', secondary='favorite_character')

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            #"planets": self.planets,
            #"characters": self.characters
        }

    def new_user(self):
        db.session.add(self)
        db.session.commit()    

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    properties =  db.Column(db.Text , nullable=False)
    users = db.relationship('User', secondary='favorite_character')

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "properties": self.properties,
            "user": self.users
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    properties =  db.Column(db.Text , nullable=False) 
    users = db.relationship('User', secondary='favorite_planet') 

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "properties": self.properties
        }

