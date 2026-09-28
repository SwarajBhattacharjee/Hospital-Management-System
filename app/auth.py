"""
auth.py
Session-based authentication and role-based access control (RBAC).
Uses Werkzeug password hashing and clean Python decorators.
"""

from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify, abort
from app.models import User
from app.forms import LoginForm

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """
    Decorator requiring the user to be authenticated in the session.
    Returns 401 JSON if accessed via /api, else redirects to login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api'):
                return jsonify({'error': 'Unauthorized', 'message': 'Authentication required.'}), 401
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator restricting route access to specified roles (e.g., 'admin', 'doctor', 'receptionist').
    Returns 403 JSON if accessed via /api, else renders 403 error page.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                if request.path.startswith('/api'):
                    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required.'}), 401
                flash('Please log in first.', 'warning')
                return redirect(url_for('auth.login', next=request.url))

            user_role = session.get('role')
            if user_role not in allowed_roles:
                if request.path.startswith('/api'):
                    return jsonify({'error': 'Forbidden', 'message': f'Access forbidden for role: {user_role}'}), 403
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login with session initialization."""
    # If already logged in, redirect straight to dashboard
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if user and user.check_password(form.password.data):
            # Set session variables
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            flash(f"Welcome back, {user.username}! Logged in as {user.role.capitalize()}.", "success")
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('routes.dashboard'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    """Clear session data and redirect to login."""
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('auth.login'))
