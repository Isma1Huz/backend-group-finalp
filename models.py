from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize the database
db = SQLAlchemy()

# Define the User model
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    profile_info = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the one-to-many relationship with courses (instructor)
    courses = db.relationship('Course', backref='instructor', lazy=True)

    # Define the many-to-many relationship with enrollments
    enrollments = db.relationship('Enrollment', backref='user', lazy=True)

    def __init__(self, username, password, email, profile_info=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email
        self.profile_info = profile_info

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'profile_info': self.profile_info,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Define the Course model
class Course(db.Model):
    __tablename__ = 'courses'

    course_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    enrollment_limit = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    contents = db.relationship('CourseContent', backref='course', lazy=True)

    def as_dict(self):
        return {
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'instructor_id': self.instructor_id,
            'enrollment_limit': self.enrollment_limit,
            'created_at': self.created_at
        }

# Define the Enrollment model
class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    enrollment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {
            'enrollment_id': self.enrollment_id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'enrollment_date': self.enrollment_date
        }

# Define the CourseContent model
class CourseContent(db.Model):
    __tablename__ = 'course_contents'

    content_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    topic = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def as_dict(self):
        return {
            'content_id': self.content_id,
            'course_id': self.course_id,
            'topic': self.topic,
            'content': self.content
        }
    

