"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import db, Character, Favorite_character
from models import db, Planet, Favorite_planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
#USUARIO----------------------------------------------------------------------------------------------------------
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()

    user = User()
    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]
            
    user.new_user()  
    
    return jsonify({"usuario" : user.serialize()}), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200 
#FAV_USUARIO-----------------------------------------------------------------------------------------------------
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    
    favortie_character = Favorite_character.query.all()
    favortie_character = list(map(lambda favortie_character: favortie_character.serialize(), favortie_character))
    favortie_planet = Favorite_planet.query.all()
    favortie_planet = list(map(lambda favortie_planet: favortie_planet.serialize(), favortie_planet))

    return jsonify(favortie_character, favortie_planet), 200  
#AGREGAR_FAV-----------------------------------------------------------------------------------------------------
@app.route('/favorite_planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    data = request.get_json()

    favorite_planet = Favorite_planet()
    favorite_planet.user_id = data ['user_id']
    favorite_planet.planet_id = planet_id 
    favorite_planet.new_favorite_planet()

    return jsonify({"msg":"added favorite_planet"}), 201

@app.route('/favorite_character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    data = request.get_json()

    favorite_character = Favorite_character()
    favorite_character.user_id = data ['user_id']
    favorite_character.character_id = character_id
    favorite_character.new_favorite_character()

    return jsonify({"msg":"added favorite_character"}), 201
#PLANETAS-----------------------------------------------------------------------------------------------------
@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()

    planet = Planet()
    planet.name = data["name"]
    planet.properties = data["properties"] 
    planet.new_planet()

    return jsonify({"msg":"planet created"}), 201

@app.route('/planets', methods=['GET'])
def get_all_panets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))# convertir en array

    return jsonify(planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    
    if planet is not None:
        return jsonify({"planet": planet.serialize()}), 200
    
    else:
        return jsonify({ "msg": "planet not found"}), 404
#PERSONAJES-----------------------------------------------------------------------------------------------------
@app.route('/characters', methods=['POST'])
def add_character():
    data = request.get_json()

    character = Character()
    character.name = data["name"]
    character.properties = data["properties"] 
    character.new_character()

    return jsonify({"msg":"character created"}), 201

@app.route('/characters', methods=['GET'])
def get_all_character():
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))

    return jsonify(characters), 200  

@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get(id)
    
    if character is not None:
        return jsonify({"character" : character.serialize()}), 200
    
    else:
        return jsonify({ "msg": "character not found"}), 404
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)