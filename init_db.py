"""
init_db.py
Database initialization and idempotent seed script for Hospital Management System.
Creates all database tables and seeds demo users, doctors, patients, staff, and appointments.
"""

from datetime import date, time
from app import create_app
from app.models import db, User, Doctor, Patient, Appointment, Staff


def seed_database():
    """Idempotently seed essential demo data and initial test records."""
    app = create_app()

    with app.app_context():
        # Ensure all tables exist
        db.create_all()
        print("[INIT] Database tables verified / created.")

        # -------------------------------------------------------------
        # 1. SEED DEMO USERS (Idempotent)
        # -------------------------------------------------------------
        demo_users = [
            {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
            {'username': 'doctor', 'password': 'doctor123', 'role': 'doctor'},
            {'username': 'receptionist', 'password': 'receptionist123', 'role': 'receptionist'},
        ]

        for user_data in demo_users:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                new_user = User(username=user_data['username'], role=user_data['role'])
                new_user.set_password(user_data['password'])
                db.session.add(new_user)
                print(f"[SEED] Created demo user: {user_data['username']} ({user_data['role']})")
            else:
                # Update password hash in case it changed
                existing_user.set_password(user_data['password'])
                existing_user.role = user_data['role']
                print(f"[EXISTS] User '{user_data['username']}' already present.")

        db.session.commit()

        # -------------------------------------------------------------
        # 2. SEED SAMPLE DOCTORS
        # -------------------------------------------------------------
        sample_doctors = [
            {
                'name': 'Sarah Jenkins',
                'specialization': 'Cardiology',
                'phone': '9876543210',
                'email': 's.jenkins@pulsecare.org',
                'available_days': 'Monday, Wednesday, Friday (09:00 - 14:00)'
            },
            {
                'name': 'Alan Turing',
                'specialization': 'Neurology',
                'phone': '9876543211',
                'email': 'a.turing@pulsecare.org',
                'available_days': 'Tuesday, Thursday, Saturday (10:00 - 16:00)'
            },
            {
                'name': 'Grace Hopper',
                'specialization': 'Pediatrics',
                'phone': '9876543212',
                'email': 'g.hopper@pulsecare.org',
                'available_days': 'Monday to Friday (08:30 - 13:30)'
            }
        ]

        for doc_data in sample_doctors:
            if not Doctor.query.filter_by(email=doc_data['email']).first():
                doctor = Doctor(**doc_data)
                db.session.add(doctor)
                print(f"[SEED] Added doctor: Dr. {doc_data['name']} ({doc_data['specialization']})")

        db.session.commit()

        # -------------------------------------------------------------
        # 3. SEED SAMPLE PATIENTS
        # -------------------------------------------------------------
        sample_patients = [
            {
                'name': 'John Doe',
                'age': 38,
                'gender': 'Male',
                'phone': '9123456780',
                'email': 'john.doe@example.com',
                'address': '221B Baker St, London',
                'blood_group': 'O+'
            },
            {
                'name': 'Jane Smith',
                'age': 29,
                'gender': 'Female',
                'phone': '9123456781',
                'email': 'jane.smith@example.com',
                'address': '42 Wallaby Way, Sydney',
                'blood_group': 'A+'
            },
            {
                'name': 'Carlos Santana',
                'age': 52,
                'gender': 'Male',
                'phone': '9123456782',
                'email': 'carlos.santana@example.com',
                'address': '742 Evergreen Terrace, Springfield',
                'blood_group': 'B-'
            }
        ]

        for pat_data in sample_patients:
            if not Patient.query.filter_by(email=pat_data['email']).first():
                patient = Patient(**pat_data)
                db.session.add(patient)
                print(f"[SEED] Added patient: {pat_data['name']}")

        db.session.commit()

        # -------------------------------------------------------------
        # 4. SEED SAMPLE STAFF
        # -------------------------------------------------------------
        sample_staff = [
            {
                'name': 'Robert Johnson',
                'role': 'Nurse Manager',
                'phone': '9811223344',
                'email': 'r.johnson@pulsecare.org'
            },
            {
                'name': 'Emily Davis',
                'role': 'Laboratory Technician',
                'phone': '9811223345',
                'email': 'e.davis@pulsecare.org'
            }
        ]

        for st_data in sample_staff:
            if not Staff.query.filter_by(email=st_data['email']).first():
                staff_member = Staff(**st_data)
                db.session.add(staff_member)
                print(f"[SEED] Added staff member: {st_data['name']} ({st_data['role']})")

        db.session.commit()

        # -------------------------------------------------------------
        # 5. SEED INITIAL APPOINTMENTS
        # -------------------------------------------------------------
        p1 = Patient.query.filter_by(email='john.doe@example.com').first()
        d1 = Doctor.query.filter_by(email='s.jenkins@pulsecare.org').first()

        if p1 and d1:
            existing_apt = Appointment.query.filter_by(patient_id=p1.id, doctor_id=d1.id).first()
            if not existing_apt:
                apt = Appointment(
                    patient_id=p1.id,
                    doctor_id=d1.id,
                    date=date(2026, 10, 5),
                    time=time(10, 30),
                    reason="Routine Cardiology Consultation and ECG Review",
                    status="Scheduled"
                )
                db.session.add(apt)
                print(f"[SEED] Scheduled sample appointment for {p1.name} with Dr. {d1.name}")

        db.session.commit()
        print("[SUCCESS] Database initialization and idempotent seeding complete.")


if __name__ == '__main__':
    seed_database()
