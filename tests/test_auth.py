"""
test_auth.py
Unit and integration tests for authentication and role-based access control.
"""

def test_login_success(client, auth):
    """Test successful login for admin user."""
    response = auth.login('admin', 'admin123')
    assert response.status_code == 200
    assert b"Hospital Overview" in response.data
    assert b"admin (admin)" in response.data


def test_login_invalid_password(client, auth):
    """Test login failure with wrong password."""
    response = auth.login('admin', 'wrongpass')
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_login_nonexistent_user(client, auth):
    """Test login failure with unknown user."""
    response = auth.login('unknown_user', 'pass123')
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_logout(client, auth):
    """Test logout clears session and redirects."""
    auth.login('admin', 'admin123')
    response = auth.logout()
    assert response.status_code == 200
    assert b"You have been successfully logged out" in response.data


def test_unauthorized_redirect(client):
    """Unauthenticated users should be redirected to login."""
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page" in response.data


def test_receptionist_cannot_access_staff(client, auth):
    """Receptionist role must receive 403 Forbidden when accessing /staff."""
    auth.login('receptionist', 'receptionist123')
    response = client.get('/staff')
    assert response.status_code == 403
    assert b"403 - Forbidden" in response.data


def test_doctor_cannot_add_patients(client, auth):
    """Doctor role is view-only for patient creation and receives 403."""
    auth.login('doctor', 'doctor123')
    response = client.get('/patients/new')
    assert response.status_code == 403
