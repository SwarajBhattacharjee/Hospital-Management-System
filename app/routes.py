"""
routes.py
Main web UI routes for the Hospital Management System.
Handles rendering HTML templates, CRUD workflows, role enforcement, and validation.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, abort
from app.models import db, Patient, Doctor, Appointment, Staff, User
from app.auth import login_required, role_required
from app.forms import PatientForm, DoctorForm, AppointmentForm, StaffForm
from sqlalchemy import or_

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def index():
    """Root URL redirects authenticated users to dashboard, others to login."""
    if 'user_id' in session:
        return redirect(url_for('routes.dashboard'))
    return redirect(url_for('auth.login'))


@routes_bp.route('/dashboard')
@login_required
def dashboard():
    """Main administrative dashboard with metric counters and recent appointments."""
    patient_count = Patient.query.count()
    doctor_count = Doctor.query.count()
    appointment_count = Appointment.query.count()
    staff_count = Staff.query.count()

    recent_appointments = (
        Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'dashboard.html',
        patient_count=patient_count,
        doctor_count=doctor_count,
        appointment_count=appointment_count,
        staff_count=staff_count,
        recent_appointments=recent_appointments
    )


# ==========================================
# PATIENTS MODULE
# ==========================================

@routes_bp.route('/patients')
@login_required
def patients():
    """List all patients with optional search by name, phone, or email."""
    query = request.args.get('q', '').strip()
    if query:
        patient_list = Patient.query.filter(
            or_(
                Patient.name.ilike(f'%{query}%'),
                Patient.phone.ilike(f'%{query}%'),
                Patient.email.ilike(f'%{query}%')
            )
        ).order_by(Patient.name.asc()).all()
    else:
        patient_list = Patient.query.order_by(Patient.name.asc()).all()

    return render_template('patients.html', patients=patient_list, query=query)


@routes_bp.route('/patients/<int:id>')
@login_required
def patient_detail(id):
    """View detailed information and appointment history for a specific patient."""
    patient = db.get_or_404(Patient, id)
    appointments = (
        Appointment.query.filter_by(patient_id=patient.id)
        .order_by(Appointment.date.desc(), Appointment.time.desc())
        .all()
    )
    return render_template('patient_detail.html', patient=patient, appointments=appointments)


@routes_bp.route('/patients/new', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'receptionist')
def new_patient():
    """Register a new patient."""
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            name=form.name.data.strip(),
            age=form.age.data,
            gender=form.gender.data,
            phone=form.phone.data.strip(),
            email=form.email.data.strip().lower(),
            blood_group=form.blood_group.data,
            address=form.address.data.strip() if form.address.data else ''
        )
        db.session.add(patient)
        db.session.commit()
        flash(f'Patient "{patient.name}" successfully registered!', 'success')
        return redirect(url_for('routes.patient_detail', id=patient.id))

    return render_template('patient_form.html', form=form, title='Register New Patient')


@routes_bp.route('/patients/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'receptionist')
def edit_patient(id):
    """Edit an existing patient's details."""
    patient = db.get_or_404(Patient, id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        patient.name = form.name.data.strip()
        patient.age = form.age.data
        patient.gender = form.gender.data
        patient.phone = form.phone.data.strip()
        patient.email = form.email.data.strip().lower()
        patient.blood_group = form.blood_group.data
        patient.address = form.address.data.strip() if form.address.data else ''

        db.session.commit()
        flash(f'Patient "{patient.name}" updated successfully.', 'success')
        return redirect(url_for('routes.patient_detail', id=patient.id))

    return render_template('patient_form.html', form=form, title=f'Edit Patient: {patient.name}')


@routes_bp.route('/patients/<int:id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_patient(id):
    """Delete a patient record. Blocked if the patient has appointments."""
    patient = db.get_or_404(Patient, id)
    if patient.appointments:
        flash(
            f'Cannot delete patient "{patient.name}" because they have existing appointment records. Cancel or remove appointments first.',
            'danger'
        )
        return redirect(url_for('routes.patient_detail', id=patient.id))

    db.session.delete(patient)
    db.session.commit()
    flash(f'Patient "{patient.name}" has been deleted.', 'info')
    return redirect(url_for('routes.patients'))


# ==========================================
# DOCTORS MODULE
# ==========================================

@routes_bp.route('/doctors')
@login_required
def doctors():
    """List all registered doctors and their specializations."""
    doctor_list = Doctor.query.order_by(Doctor.name.asc()).all()
    return render_template('doctors.html', doctors=doctor_list)


@routes_bp.route('/doctors/new', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def new_doctor():
    """Add a new doctor to the hospital roster (Admin only)."""
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(
            name=form.name.data.strip(),
            specialization=form.specialization.data.strip(),
            phone=form.phone.data.strip(),
            email=form.email.data.strip().lower(),
            available_days=form.available_days.data.strip()
        )
        db.session.add(doctor)
        db.session.commit()
        flash(f'Dr. {doctor.name} added successfully.', 'success')
        return redirect(url_for('routes.doctors'))

    return render_template('doctor_form.html', form=form, title='Add New Doctor')


@routes_bp.route('/doctors/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_doctor(id):
    """Edit doctor profile (Admin only)."""
    doctor = db.get_or_404(Doctor, id)
    form = DoctorForm(obj=doctor)
    if form.validate_on_submit():
        doctor.name = form.name.data.strip()
        doctor.specialization = form.specialization.data.strip()
        doctor.phone = form.phone.data.strip()
        doctor.email = form.email.data.strip().lower()
        doctor.available_days = form.available_days.data.strip()

        db.session.commit()
        flash(f'Dr. {doctor.name} profile updated.', 'success')
        return redirect(url_for('routes.doctors'))

    return render_template('doctor_form.html', form=form, title=f'Edit Doctor: Dr. {doctor.name}')


@routes_bp.route('/doctors/<int:id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_doctor(id):
    """Delete a doctor. Blocked if the doctor has existing appointments."""
    doctor = db.get_or_404(Doctor, id)
    if doctor.appointments:
        flash(
            f'Cannot delete Dr. {doctor.name} because they have scheduled appointments. Reassign or cancel them first.',
            'danger'
        )
        return redirect(url_for('routes.doctors'))

    db.session.delete(doctor)
    db.session.commit()
    flash(f'Dr. {doctor.name} deleted successfully.', 'info')
    return redirect(url_for('routes.doctors'))


# ==========================================
# APPOINTMENTS MODULE
# ==========================================

@routes_bp.route('/appointments')
@login_required
def appointments():
    """List all appointments with status filtering."""
    status_filter = request.args.get('status', '').strip()
    query = Appointment.query
    if status_filter in ['Scheduled', 'Completed', 'Cancelled']:
        query = query.filter_by(status=status_filter)

    appointment_list = query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('appointments.html', appointments=appointment_list, current_filter=status_filter)


@routes_bp.route('/appointments/new', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'receptionist')
def new_appointment():
    """Schedule a new appointment, preventing doctor double-booking."""
    form = AppointmentForm()

    # Populate select dropdown choices dynamically from database
    patients = Patient.query.order_by(Patient.name.asc()).all()
    doctors = Doctor.query.order_by(Doctor.name.asc()).all()

    form.patient_id.choices = [(p.id, f"{p.name} (Phone: {p.phone})") for p in patients]
    form.doctor_id.choices = [(d.id, f"Dr. {d.name} ({d.specialization})") for d in doctors]

    # Pre-select patient if provided in query string
    prefill_patient = request.args.get('patient_id', type=int)
    if request.method == 'GET' and prefill_patient:
        form.patient_id.data = prefill_patient

    if form.validate_on_submit():
        # Check for doctor double booking: same doctor, same date, same time, non-cancelled
        conflict = Appointment.query.filter(
            Appointment.doctor_id == form.doctor_id.data,
            Appointment.date == form.date.data,
            Appointment.time == form.time.data,
            Appointment.status != 'Cancelled'
        ).first()

        if conflict:
            flash(
                f"Double-booking conflict! Dr. {conflict.doctor.name} is already booked on {form.date.data} at {form.time.data.strftime('%H:%M')}.",
                "danger"
            )
            return render_template('appointment_form.html', form=form, title='Schedule Appointment')

        appointment = Appointment(
            patient_id=form.patient_id.data,
            doctor_id=form.doctor_id.data,
            date=form.date.data,
            time=form.time.data,
            reason=form.reason.data.strip(),
            status=form.status.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment successfully scheduled!', 'success')
        return redirect(url_for('routes.appointments'))

    return render_template('appointment_form.html', form=form, title='Schedule Appointment')


@routes_bp.route('/appointments/<int:id>/status', methods=['POST'])
@login_required
@role_required('admin', 'receptionist', 'doctor')
def update_appointment_status(id):
    """Update status of an appointment (Scheduled, Completed, Cancelled)."""
    appointment = db.get_or_404(Appointment, id)
    new_status = request.form.get('status')
    if new_status in ['Scheduled', 'Completed', 'Cancelled']:
        appointment.status = new_status
        db.session.commit()
        flash(f'Appointment #{appointment.id} status changed to {new_status}.', 'success')
    else:
        flash('Invalid status provided.', 'danger')

    return redirect(request.referrer or url_for('routes.appointments'))


# ==========================================
# STAFF MODULE (Admin Only)
# ==========================================

@routes_bp.route('/staff')
@login_required
@role_required('admin')
def staff():
    """List all staff members (Admin only)."""
    staff_list = Staff.query.order_by(Staff.name.asc()).all()
    return render_template('staff.html', staff=staff_list)


@routes_bp.route('/staff/new', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def new_staff():
    """Add a new staff member (Admin only)."""
    form = StaffForm()
    if form.validate_on_submit():
        member = Staff(
            name=form.name.data.strip(),
            role=form.role.data.strip(),
            phone=form.phone.data.strip(),
            email=form.email.data.strip().lower()
        )
        db.session.add(member)
        db.session.commit()
        flash(f'Staff member "{member.name}" added successfully.', 'success')
        return redirect(url_for('routes.staff'))

    return render_template('staff_form.html', form=form, title='Add Staff Member')


@routes_bp.route('/staff/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_staff(id):
    """Edit staff member details (Admin only)."""
    member = db.get_or_404(Staff, id)
    form = StaffForm(obj=member)
    if form.validate_on_submit():
        member.name = form.name.data.strip()
        member.role = form.role.data.strip()
        member.phone = form.phone.data.strip()
        member.email = form.email.data.strip().lower()

        db.session.commit()
        flash(f'Staff member "{member.name}" updated successfully.', 'success')
        return redirect(url_for('routes.staff'))

    return render_template('staff_form.html', form=form, title=f'Edit Staff: {member.name}')


@routes_bp.route('/staff/<int:id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_staff(id):
    """Delete a staff member (Admin only)."""
    member = db.get_or_404(Staff, id)
    db.session.delete(member)
    db.session.commit()
    flash(f'Staff member "{member.name}" has been removed.', 'info')
    return redirect(url_for('routes.staff'))


# ==========================================
# API DOCUMENTATION PAGE
# ==========================================

@routes_bp.route('/api-docs')
@login_required
def api_docs():
    """Interactive documentation page listing all available REST API endpoints."""
    return render_template('api_docs.html')
