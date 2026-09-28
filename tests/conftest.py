"""
conftest.py
Pytest fixtures for the Hospital Management System test suite.
Provides isolated in-memory test database, test client, and authentication helpers.
"""

import pytest
from app import create_app
from app.models import db, User, Patient, Doctor, Appointment, Staff


@pytest.fixture
def app():
    """Create and configure a clean, isolated application instance for testing."""
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,  # Disabled for unit testing form submissions
        'SECRET_KEY': 'test-secret-key-12345'
    }
    app = create_app(test_config)

    with app.app_context():
        db.create_all()

        # Seed standard test users
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')

        doc_user = User(username='doctor', role='doctor')
        doc_user.set_password('doctor123')

        rec_user = User(username='receptionist', role='receptionist')
        rec_user.set_password('receptionist123')

        db.session.add_all([admin, doc_user, rec_user])

        # Seed sample doctor and patient for testing
        doc = Doctor(
            name='Test Doctor',
            specialization='General Medicine',
            phone='9998887770',
            email='doc@test.com',
            available_days='Monday to Friday'
        )
        pat = Patient(
            name='Test Patient',
            age=30,
            gender='Male',
            phone='9998887771',
            email='patient@test.com',
            blood_group='O+',
            address='123 Test St'
        )
        staff = Staff(
            name='Test Staff',
            role='Nurse',
            phone='9998887772',
            email='staff@test.com'
        )
        db.session.add_all([doc, pat, staff])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the application."""
    return app.test_client()


class AuthActions:
    """Helper class to authenticate test sessions with specific roles."""
    def __init__(self, client):
        self._client = client

    def login(self, username='admin', password='admin123'):
        return self._client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)

    def logout(self):
        return self._client.get('/logout', follow_redirects=True)


@pytest.fixture
def auth(client):
    """Fixture providing authentication helpers."""
    return AuthActions(client)
