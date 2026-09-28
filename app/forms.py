"""
forms.py
Flask-WTF forms with comprehensive validation.
Includes forms for Login, Patients, Doctors, Appointments, and Staff.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, PasswordField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, Optional

# Blood group options for medical standard records
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-')
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
]

STATUS_CHOICES = [
    ('Scheduled', 'Scheduled'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled')
]


class LoginForm(FlaskForm):
    """User login form."""
    username = StringField(
        'Username',
        validators=[DataRequired(message="Username is required."), Length(max=64)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Password is required.")]
    )
    submit = SubmitField('Sign In')


class PatientForm(FlaskForm):
    """Patient registration and edit form with strict field validations."""
    name = StringField(
        'Full Name',
        validators=[
            DataRequired(message="Patient name is required."),
            Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
        ]
    )
    age = IntegerField(
        'Age',
        validators=[
            DataRequired(message="Age is required."),
            NumberRange(min=0, max=120, message="Age must be between 0 and 120.")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=GENDER_CHOICES,
        validators=[DataRequired(message="Please select a gender.")]
    )
    phone = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Phone number is required."),
            Regexp(r'^[0-9]{7,15}$', message="Phone must be between 7 and 15 digits.")
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    blood_group = SelectField(
        'Blood Group',
        choices=BLOOD_GROUP_CHOICES,
        validators=[DataRequired(message="Please select a valid blood group.")]
    )
    address = TextAreaField(
        'Address',
        validators=[Optional(), Length(max=500)]
    )
    submit = SubmitField('Save Patient')


class DoctorForm(FlaskForm):
    """Doctor registration and profile editing form."""
    name = StringField(
        'Doctor Name',
        validators=[
            DataRequired(message="Doctor name is required."),
            Length(min=2, max=100, message="Name must be between 2 and 100 characters.")
        ]
    )
    specialization = StringField(
        'Specialization',
        validators=[
            DataRequired(message="Specialization is required."),
            Length(min=2, max=100)
        ]
    )
    phone = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Phone number is required."),
            Regexp(r'^[0-9]{7,15}$', message="Phone must be between 7 and 15 digits.")
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    available_days = StringField(
        'Available Days',
        validators=[
            DataRequired(message="Available days are required (e.g. Mon, Wed, Fri)."),
            Length(max=100)
        ]
    )
    submit = SubmitField('Save Doctor')


class AppointmentForm(FlaskForm):
    """Appointment scheduling form with patient and doctor selection."""
    patient_id = SelectField(
        'Select Patient',
        coerce=int,
        validators=[DataRequired(message="Please select a patient.")]
    )
    doctor_id = SelectField(
        'Select Doctor',
        coerce=int,
        validators=[DataRequired(message="Please select a doctor.")]
    )
    date = DateField(
        'Appointment Date',
        validators=[DataRequired(message="Appointment date is required.")]
    )
    time = TimeField(
        'Appointment Time',
        validators=[DataRequired(message="Appointment time is required.")]
    )
    reason = StringField(
        'Reason for Visit',
        validators=[
            DataRequired(message="Reason for visit is required."),
            Length(min=3, max=255, message="Reason must be between 3 and 255 characters.")
        ]
    )
    status = SelectField(
        'Status',
        choices=STATUS_CHOICES,
        default='Scheduled',
        validators=[DataRequired()]
    )
    submit = SubmitField('Save Appointment')


class StaffForm(FlaskForm):
    """Staff member profile form (Admin only)."""
    name = StringField(
        'Staff Name',
        validators=[
            DataRequired(message="Staff name is required."),
            Length(min=2, max=100)
        ]
    )
    role = StringField(
        'Staff Role / Designation',
        validators=[
            DataRequired(message="Staff role is required (e.g., Nurse, Lab Tech, Accountant)."),
            Length(min=2, max=50)
        ]
    )
    phone = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Phone number is required."),
            Regexp(r'^[0-9]{7,15}$', message="Phone must be between 7 and 15 digits.")
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    submit = SubmitField('Save Staff Member')
