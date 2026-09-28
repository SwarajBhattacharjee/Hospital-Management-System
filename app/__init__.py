"""
__init__.py
Application factory for Hospital Management System.
Configures logging, database, CSRF protection, error handling, and health probes.
"""

import os
import sys
import logging
from flask import Flask, jsonify, render_template, request, session
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import text
from app.models import db

# Initialize CSRF extension
csrf = CSRFProtect()


def create_app(test_config=None):
    """
    Application factory pattern.
    Configures and creates the Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Ensure the instance folder exists for SQLite storage
    os.makedirs(app.instance_path, exist_ok=True)

    # -------------------------------------------------------------
    # LOGGING CONFIGURATION (stdout with timestamp and log level)
    # -------------------------------------------------------------
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    logger = logging.getLogger(__name__)

    # -------------------------------------------------------------
    # ENVIRONMENT CONFIGURATION & SECURITY FALLBACK
    # -------------------------------------------------------------
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        secret_key = 'dev-secret-key-only-change-in-production'
        logger.warning(
            "WARNING: SECRET_KEY environment variable is not set! Using labeled dev-only fallback. "
            "Please configure SECRET_KEY in your production environment."
        )

    # Default DB: SQLite at an absolute path in the instance folder
    default_db_path = os.path.join(app.instance_path, 'hospital.db')
    database_url = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.abspath(default_db_path)}"

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        DEBUG=False,  # Debug disabled by default
        TESTING=False
    )

    # Override config if test_config is provided (used for pytest)
    if test_config:
        app.config.update(test_config)

    # -------------------------------------------------------------
    # EXTENSIONS INITIALIZATION
    # -------------------------------------------------------------
    db.init_app(app)
    csrf.init_app(app)

    # -------------------------------------------------------------
    # BLUEPRINT REGISTRATION
    # -------------------------------------------------------------
    from app.auth import auth_bp
    from app.routes import routes_bp
    from app.api import api_bp

    # Exempt the REST API blueprint from CSRF protection
    csrf.exempt(api_bp)

    app.register_blueprint(auth_bp)
    app.register_blueprint(routes_bp)
    app.register_blueprint(api_bp)

    # -------------------------------------------------------------
    # TEMPLATE CONTEXT PROCESSOR (Inject current_user into all views)
    # -------------------------------------------------------------
    @app.context_processor
    def inject_current_user():
        """Makes current_user available to all Jinja2 templates."""
        user = None
        if 'user_id' in session:
            user = {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'role': session.get('role')
            }
        return {'current_user': user}

    # -------------------------------------------------------------
    # HEALTH CHECK PROBE (Public endpoint)
    # -------------------------------------------------------------
    @app.route('/health', methods=['GET'])
    def health():
        """
        Health probe verifying application and database connectivity.
        Returns 200 {"status": "healthy"} or 503 {"status": "unhealthy"} on failure.
        """
        try:
            # Ping database to confirm connectivity
            db.session.execute(text('SELECT 1'))
            return jsonify({'status': 'healthy'}), 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return jsonify({'status': 'unhealthy', 'error': 'Database unreachable'}), 503

    # -------------------------------------------------------------
    # CUSTOM ERROR HANDLERS
    # -------------------------------------------------------------
    @app.errorhandler(403)
    def forbidden_error(error):
        if request.path.startswith('/api'):
            return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to access this resource.'}), 403
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        if request.path.startswith('/api'):
            return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f"Internal server error: {error}")
        if request.path.startswith('/api'):
            return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred.'}), 500
        return render_template('500.html'), 500

    # -------------------------------------------------------------
    # AUTOMATIC DATABASE TABLE CREATION
    # -------------------------------------------------------------
    with app.app_context():
        db.create_all()

    return app
