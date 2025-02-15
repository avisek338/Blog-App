from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    # Initialize the app
    app = Flask(__name__)

    # Set configuration
    #basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # with app.app_context():
    #     db.drop_all()
       

    # Set the login view for Flask-Login
    login_manager.login_view = 'users.login'

    # Register blueprints
    from MyBlog.core.views import core
    from MyBlog.users.views import users
    from MyBlog.error_pages.handlers import error_pages
    from MyBlog.blog_posts.views import blog_posts
    

    app.register_blueprint(core)
    app.register_blueprint(users)
    app.register_blueprint(blog_posts)

    app.register_blueprint(error_pages)

    return app
