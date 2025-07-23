from flask import Flask, request, g
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config
import logging
import time
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    
    request_logger = logging.getLogger('request_tracker')
    request_logger.setLevel(logging.INFO)
    
    return request_logger

def create_app():
    app = Flask(__name__)

    request_logger = setup_logging()
    
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    @app.before_request
    def log_request_info():
        g.start_time = time.time()
        request_logger.info(f"REQUEST: {request.method} {request.url} | IP: {request.remote_addr} | User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    @app.after_request
    def log_response_info(response):
        duration = time.time() - g.start_time
        request_logger.info(f"RESPONSE: {response.status_code} | Duration: {duration:.3f}s | Route: {request.endpoint}")
        return response
    
    @app.errorhandler(400)
    def bad_request(error):
        app.logger.error(f"Bad Request (400): {request.url} | Error: {str(error)}")
        return {'message': 'Bad request'}, 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        app.logger.warning(f"Unauthorized (401): {request.url} | IP: {request.remote_addr}")
        return {'message': 'Authentication required'}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        app.logger.warning(f"Forbidden (403): {request.url} | IP: {request.remote_addr}")
        return {'message': 'Access forbidden'}, 403
    
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning(f"Not Found (404): {request.url}")
        return {'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f"Internal Server Error (500): {request.url} | Error: {str(error)}")
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.warning(f"Expired token used: {request.url} | IP: {request.remote_addr}")
        return {'message': 'Token has expired'}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        app.logger.warning(f"Invalid token used: {request.url} | IP: {request.remote_addr} | Error: {error}")
        return {'message': 'Invalid token'}, 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        app.logger.warning(f"Missing token: {request.url} | IP: {request.remote_addr}")
        return {'message': 'Authorization token is required'}, 401
    
    from app.routes.user_route import user_bp
    from app.routes.inspection_route import inspection_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/v1/')
    app.register_blueprint(inspection_bp, url_prefix='/api/v1/')

    with app.app_context():
        from app.models import user, inspection
        db.create_all()
        app.logger.info("Database tables created successfully")

    app.logger.info("Flask application initialized successfully")
    return app