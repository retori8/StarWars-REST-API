from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120),  nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    favorite_planets = db.relationship('Favorite_planet', backref='user')
    favorite_characters = db.relationship('Favorite_character', backref='user')

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    def new_user(self):
        db.session.add(self)
        db.session.commit()    

    def update_user(self):
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()    

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    properties =  db.Column(db.Text , nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "properties": self.properties,
        }
    
    def new_character(self):
        db.session.add(self)
        db.session.commit()   

    def delete_character(self):
        db.session.delete(self)
        db.session.commit()     

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    properties =  db.Column(db.Text , nullable=False) 

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "properties": self.properties
        }
    
    def new_planet(self):
        db.session.add(self)
        db.session.commit()  

    def delete_planet(self):
        db.session.delete(self)
        db.session.commit() 
        

class Favorite_character(db.Model):
    __tablename__ = 'favorite_character' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    characters = db.relationship('Character', backref='favorite_character')

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }
    
    def new_favorite_character(self):
        db.session.add(self)
        db.session.commit()

    def delete_favorite_character(self):
        db.session.delete(self)
        db.session.commit()    


class Favorite_planet(db.Model):
    __tablename__ = 'favorite_planet'
    id = db.Column(db.Integer, primary_key=True)    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))    
    planets = db.relationship('Planet', backref='favorite_planet')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }      

    def new_favorite_planet(self):
        db.session.add(self)
        db.session.commit()  

    def delete_favorite_planet(self):
        db.session.delete(self)
        db.session.commit()     

