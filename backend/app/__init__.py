from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)

    # Configuration via config classes
    from .config import get_config
    config_obj = get_config(os.environ.get('APP_CONFIG', 'development'))
    app.config.from_object(config_obj)

    # Fallbacks for compatibility
    app.config.setdefault('SECRET_KEY', os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production'))
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', os.environ.get('DATABASE_URL', 'sqlite:///bep_app.db'))
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    app.config.setdefault('JWT_SECRET_KEY', os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production'))
    app.config.setdefault('JWT_ACCESS_TOKEN_EXPIRES', timedelta(hours=int(os.environ.get('JWT_ACCESS_TOKEN_HOURS', '24'))))
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    
    # Configure CORS to handle preflight requests properly
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001')
    CORS(app, resources={
        r"/api/*": {
            "origins": [o.strip() for o in cors_origins.split(',') if o.strip()],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Configure Flask to handle URLs with and without trailing slashes
    app.url_map.strict_slashes = False
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.projects import projects_bp
    from .routes.goals import goals_bp
    from .routes.tidp import tidp_bp
    from .routes.comments import comments_bp
    from .routes.reports import reports_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')
    app.register_blueprint(tidp_bp, url_prefix='/api/tidp')
    app.register_blueprint(comments_bp, url_prefix='/api/comments')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    
    # Configure logging
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

    return app
