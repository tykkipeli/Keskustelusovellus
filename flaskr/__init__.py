from flask import Flask
from dotenv import load_dotenv
from .views import auth, home, area, thread, message
from .database import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(area.bp)
    app.register_blueprint(thread.bp)
    app.register_blueprint(message.bp)

    return app
