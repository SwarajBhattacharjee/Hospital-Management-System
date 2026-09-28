"""
api.py
REST API endpoints returning JSON responses.
Session-authenticated, exempt from CSRF protection.
Supported endpoints:
  - GET, POST /api/patients
  - GET, PUT, DELETE /api/patients/<id>
  - GET /api/doctors
  - GET /api/appointments
"""

import re
from flask import Blueprint, jsonify, request, session
from app.models import db, Patient, Doctor, Appointment
from app.auth import login_required, role_required

api_bp = Blueprint('api', __name__, url_prefix='/api')

VALID_BLOOD_GROUPS = {'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'}
VALID_GENDERS = {'Male', 'Female', 'Other'}
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PHONE_REGEX = r'^[0-9]{7,15}$'


def validate_patient_payload(data, is_update=False):
    """Validate JSON payload for patient creation and updates."""
    errors = []

    if not is_update or 'name' in data:
        name = str(data.get('name', '')).strip()
        if not name or len(name) < 2 or len(name) > 100:
            errors.append("Field 'name' must be between 2 and 100 characters.")

    if not is_update or 'age' in data:
        try:
            age = int(data.get('age', -1))
            if age < 0 or age > 120:
                errors.append("Field 'age' must be an integer between 0 and 120.")
        except (ValueError, TypeError):
            errors.append("Field 'age' must be a valid integer.")

    if not is_update or 'gender' in data:
        gender = str(data.get('gender', '')).strip()
        if gender not in VALID_GENDERS:
            errors.append(f"Field 'gender' must be one of {list(VALID_GENDERS)}.")

    if not is_update or 'phone' in data:
        phone = str(data.get('phone', '')).strip()
        if not re.match(PHONE_REGEX, phone):
            errors.append("Field 'phone' must be between 7 and 15 numeric digits.")

    if not is_update or 'email' in data:
        email = str(data.get('email', '')).strip().lower()
        if not re.match(EMAIL_REGEX, email):
            errors.append("Field 'email' must be a valid email format.")

    if not is_update or 'blood_group' in data:
        blood_group = str(data.get('blood_group', '')).strip().upper()
        if blood_group not in VALID_BLOOD_GROUPS:
            errors.append(f"Field 'blood_group' must be one of {sorted(list(VALID_BLOOD_GROUPS))}.")

    return errors


# ==========================================
# PATIENTS API
# ==========================================

@api_bp.route('/patients', methods=['GET'])
@login_required
def get_patients():
    """Retrieve all patients in JSON format."""
    patients = Patient.query.order_by(Patient.id.asc()).all()
    return jsonify({
        'status': 'success',
        'count': len(patients),
        'patients': [p.to_dict() for p in patients]
    }), 200


@api_bp.route('/patients', methods=['POST'])
@login_required
@role_required('admin', 'receptionist')
def create_patient():
    """Register a new patient via JSON payload."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Bad Request', 'message': 'Missing or invalid JSON payload.'}), 400

    errors = validate_patient_payload(data, is_update=False)
    if errors:
        return jsonify({'error': 'Validation Error', 'messages': errors}), 400

    patient = Patient(
        name=data['name'].strip(),
        age=int(data['age']),
        gender=data['gender'].strip(),
        phone=data['phone'].strip(),
        email=data['email'].strip().lower(),
        blood_group=data['blood_group'].strip().upper(),
        address=data.get('address', '').strip()
    )
    db.session.add(patient)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Patient created successfully.',
        'patient': patient.to_dict()
    }), 201


@api_bp.route('/patients/<int:id>', methods=['GET'])
@login_required
def get_patient(id):
    """Retrieve a single patient by ID."""
    patient = db.session.get(Patient, id)
    if not patient:
        return jsonify({'error': 'Not Found', 'message': f'Patient with ID {id} not found.'}), 404

    result = patient.to_dict()
    result['appointments'] = [a.to_dict() for a in patient.appointments]
    return jsonify({
        'status': 'success',
        'patient': result
    }), 200


@api_bp.route('/patients/<int:id>', methods=['PUT'])
@login_required
@role_required('admin', 'receptionist')
def update_patient(id):
    """Update patient details."""
    patient = db.session.get(Patient, id)
    if not patient:
        return jsonify({'error': 'Not Found', 'message': f'Patient with ID {id} not found.'}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Bad Request', 'message': 'Missing or invalid JSON payload.'}), 400

    errors = validate_patient_payload(data, is_update=True)
    if errors:
        return jsonify({'error': 'Validation Error', 'messages': errors}), 400

    if 'name' in data:
        patient.name = data['name'].strip()
    if 'age' in data:
        patient.age = int(data['age'])
    if 'gender' in data:
        patient.gender = data['gender'].strip()
    if 'phone' in data:
        patient.phone = data['phone'].strip()
    if 'email' in data:
        patient.email = data['email'].strip().lower()
    if 'blood_group' in data:
        patient.blood_group = data['blood_group'].strip().upper()
    if 'address' in data:
        patient.address = data['address'].strip()

    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'Patient updated successfully.',
        'patient': patient.to_dict()
    }), 200


@api_bp.route('/patients/<int:id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_patient(id):
    """Delete a patient (Admin only). Prevented if appointments exist."""
    patient = db.session.get(Patient, id)
    if not patient:
        return jsonify({'error': 'Not Found', 'message': f'Patient with ID {id} not found.'}), 404

    if patient.appointments:
        return jsonify({
            'error': 'Conflict',
            'message': f'Cannot delete patient ID {id} because existing appointments are linked to this record.'
        }), 400

    db.session.delete(patient)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': f'Patient ID {id} deleted successfully.'
    }), 200


# ==========================================
# DOCTORS & APPOINTMENTS READ-ONLY API
# ==========================================

@api_bp.route('/doctors', methods=['GET'])
@login_required
def get_doctors():
    """Retrieve all doctors."""
    doctors = Doctor.query.order_by(Doctor.name.asc()).all()
    return jsonify({
        'status': 'success',
        'count': len(doctors),
        'doctors': [d.to_dict() for d in doctors]
    }), 200


@api_bp.route('/appointments', methods=['GET'])
@login_required
def get_appointments():
    """Retrieve all appointments."""
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return jsonify({
        'status': 'success',
        'count': len(appointments),
        'appointments': [a.to_dict() for a in appointments]
    }), 200
