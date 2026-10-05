"""
test_api.py
Tests for REST API JSON endpoints, session security, status codes, and /health probe.
"""

def test_health_probe(client):
    """Test public health check endpoint returns 200 OK and healthy status."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_api_unauthorized_access(client):
    """Test that API returns 401 JSON when accessed without session."""
    response = client.get('/api/patients')
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Unauthorized'


def test_api_get_patients(client, auth):
    """Test authorized GET /api/patients returns list."""
    auth.login('receptionist', 'receptionist123')
    response = client.get('/api/patients')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'patients' in data
    assert len(data['patients']) >= 1


def test_api_create_patient_success(client, auth):
    """Test POST /api/patients with valid payload returns 201 Created."""
    auth.login('admin', 'admin123')
    payload = {
        'name': 'API Test Patient',
        'age': 35,
        'gender': 'Male',
        'phone': '9876543210',
        'email': 'api_patient@example.com',
        'blood_group': 'AB+',
        'address': 'Test City'
    }
    response = client.post('/api/patients', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['patient']['name'] == 'API Test Patient'


def test_api_create_patient_invalid_data(client, auth):
    """Test POST /api/patients with invalid age and blood group returns 400 Bad Request."""
    auth.login('admin', 'admin123')
    payload = {
        'name': 'Bad Patient',
        'age': -5,  # Invalid
        'gender': 'Male',
        'phone': '123',  # Invalid
        'email': 'not-an-email',  # Invalid
        'blood_group': 'Z+'  # Invalid
    }
    response = client.post('/api/patients', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Validation Error'
    assert len(data['messages']) >= 1


def test_api_get_single_patient(client, auth):
    """Test GET /api/patients/<id> and 404 for nonexistent ID."""
    auth.login('doctor', 'doctor123')
    response = client.get('/api/patients/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['patient']['id'] == 1

    # Nonexistent patient
    resp_404 = client.get('/api/patients/9999')
    assert resp_404.status_code == 404
    assert resp_404.get_json()['error'] == 'Not Found'


def test_api_put_patient(client, auth):
    """Test PUT /api/patients/<id> updates patient data."""
    auth.login('admin', 'admin123')
    response = client.put('/api/patients/1', json={'phone': '9876500000', 'blood_group': 'O-'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['patient']['phone'] == '9876500000'
    assert data['patient']['blood_group'] == 'O-'


def test_api_delete_patient_permissions(client, auth):
    """Test that receptionist cannot DELETE (403), but admin can (200)."""
    # Receptionist attempts DELETE -> 403 Forbidden
    auth.login('receptionist', 'receptionist123')
    resp_forbidden = client.delete('/api/patients/1')
    assert resp_forbidden.status_code == 403
    assert resp_forbidden.get_json()['error'] == 'Forbidden'
    auth.logout()

    # Admin attempts DELETE -> 200 OK
    auth.login('admin', 'admin123')
    resp_ok = client.delete('/api/patients/1')
    assert resp_ok.status_code == 200
    assert resp_ok.get_json()['status'] == 'success'


def test_api_doctors_and_appointments(client, auth):
    """Test GET /api/doctors and GET /api/appointments."""
    auth.login('doctor', 'doctor123')
    resp_doc = client.get('/api/doctors')
    assert resp_doc.status_code == 200
    assert resp_doc.get_json()['count'] >= 1

    resp_apt = client.get('/api/appointments')
    assert resp_apt.status_code == 200
    assert resp_apt.get_json()['status'] == 'success'


def test_metrics_endpoint_public_and_format(client):
    """Test public Prometheus /metrics endpoint returns 200 and text format."""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert 'text/plain' in response.content_type
    content = response.data.decode('utf-8')
    assert 'http_requests_total' in content
    assert 'http_request_duration_seconds' in content
    assert 'hms_patients_total' in content


def test_metrics_tracks_requests_and_patients(client):
    """Test that /metrics dynamically tracks patient gauge and HTTP requests."""
    # Seeded database in conftest has 1 patient
    resp1 = client.get('/metrics')
    assert resp1.status_code == 200
    content1 = resp1.data.decode('utf-8')
    assert 'hms_patients_total 1.0' in content1

    # Access health endpoint to generate request metric
    client.get('/health')

    # Verify metrics updated
    resp2 = client.get('/metrics')
    content2 = resp2.data.decode('utf-8')
    assert 'endpoint="health"' in content2
