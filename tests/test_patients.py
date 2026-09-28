"""
test_patients.py
Tests for Patient CRUD operations, data validations, and appointment rules.
"""

from datetime import date, time
from app.models import db, Patient, Appointment, Doctor


def test_create_patient_valid(client, auth):
    """Test valid patient creation via web form."""
    auth.login('admin', 'admin123')
    response = client.post('/patients/new', data={
        'name': 'Alice Walker',
        'age': 42,
        'gender': 'Female',
        'phone': '9876543210',
        'email': 'alice@walker.com',
        'blood_group': 'B+',
        'address': '456 Garden Way'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"successfully registered" in response.data
    assert b"Alice Walker" in response.data


def test_patient_validation_invalid_age(client, auth):
    """Test that invalid age (>120 or <0) is rejected."""
    auth.login('admin', 'admin123')
    response = client.post('/patients/new', data={
        'name': 'Invalid Age Patient',
        'age': 150,  # Invalid
        'gender': 'Male',
        'phone': '9876543210',
        'email': 'age@test.com',
        'blood_group': 'O+'
    })
    assert response.status_code == 200
    assert b"Age must be between 0 and 120" in response.data


def test_patient_validation_invalid_phone(client, auth):
    """Test that non-numeric or short phone numbers are rejected."""
    auth.login('admin', 'admin123')
    response = client.post('/patients/new', data={
        'name': 'Invalid Phone Patient',
        'age': 25,
        'gender': 'Male',
        'phone': '123',  # Too short (< 7 digits)
        'email': 'phone@test.com',
        'blood_group': 'AB+'
    })
    assert response.status_code == 200
    assert b"Phone must be between 7 and 15 digits" in response.data


def test_patient_delete_blocked_with_appointments(app, client, auth):
    """Test that deleting a patient with existing appointments is prevented."""
    with app.app_context():
        pat = Patient.query.filter_by(name='Test Patient').first()
        doc = Doctor.query.filter_by(name='Test Doctor').first()
        apt = Appointment(
            patient_id=pat.id,
            doctor_id=doc.id,
            date=date(2026, 11, 1),
            time=time(14, 0),
            reason='Checkup',
            status='Scheduled'
        )
        db.session.add(apt)
        db.session.commit()
        patient_id = pat.id

    auth.login('admin', 'admin123')
    response = client.post(f'/patients/{patient_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot delete patient" in response.data


def test_appointment_double_booking_rejected(app, client, auth):
    """Test that double-booking the same doctor at the same date & time is rejected."""
    auth.login('receptionist', 'receptionist123')

    with app.app_context():
        pat = Patient.query.filter_by(name='Test Patient').first()
        doc = Doctor.query.filter_by(name='Test Doctor').first()
        pat_id = pat.id
        doc_id = doc.id

    # First appointment: 2026-12-01 at 10:00 AM
    client.post('/appointments/new', data={
        'patient_id': pat_id,
        'doctor_id': doc_id,
        'date': '2026-12-01',
        'time': '10:00',
        'reason': 'First Appointment',
        'status': 'Scheduled'
    }, follow_redirects=True)

    # Second appointment for the same doctor at identical date and time
    response = client.post('/appointments/new', data={
        'patient_id': pat_id,
        'doctor_id': doc_id,
        'date': '2026-12-01',
        'time': '10:00',
        'reason': 'Second Appointment Conflict',
        'status': 'Scheduled'
    })

    assert response.status_code == 200
    assert b"Double-booking conflict" in response.data
