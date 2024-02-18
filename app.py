from flask import Flask
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

from config.db import db
from routes.auth_routes import auth_bp
from routes.notes_routes import notes_bp
from utils.crypt_utils import bcrypt

load_dotenv()

MYSQL_DB_STRING = os.getenv('MYSQL_DB_STRING')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
BASE_URL = 'api/v1'

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = JWT_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_DB_STRING
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    app.register_blueprint(auth_bp, url_prefix=f'/{BASE_URL}/auth')
    app.register_blueprint(notes_bp, url_prefix=f'/{BASE_URL}/notes')
    
    return app

app = create_app()

migrate = Migrate(app, db)
from models.User import User
from models.Note import Note, NoteShare, NoteVersion

if __name__ == '__main__':
    app.run(debug=True)