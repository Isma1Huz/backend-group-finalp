from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, User, Course, Enrollment, CourseContent

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elearning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)


migrate = Migrate(app, db)

from flask_jwt_extended import jwt_required, get_jwt_identity

class UserResource(Resource):
    @jwt_required
    def get(self, user_id):
        current_user_id = get_jwt_identity()
        if current_user_id == user_id:
            user = User.query.get(user_id)
            if user:
                return jsonify(user.as_dict())
            return {'message': 'User not found'}, 404
        return {'message': 'Unauthorized'}, 401

    @jwt_required
    def put(self, user_id):
        current_user_id = get_jwt_identity()
        if current_user_id == user_id:
            user = User.query.get(user_id)
            if user:
                data = request.get_json()
                user.username = data['username']
                user.email = data['email']
                user.profile_info = data['profile_info']
                db.session.commit()
                return jsonify(user.as_dict())
            return {'message': 'User not found'}, 404
        return {'message': 'Unauthorized'}, 401

    @jwt_required
    def delete(self, user_id):
        current_user_id = get_jwt_identity()
        if current_user_id == user_id:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return {'message': 'User deleted'}
            return {'message': 'User not found'}, 404
        return {'message': 'Unauthorized'}, 401

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Authenticate the user (you'll need to implement this logic)
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200

    return {'message': 'Invalid credentials'}, 401







class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.as_dict() for user in users])

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
        profile_info = data.get('profile_info')
        user = User(username=username, password=password, email=email, profile_info=profile_info)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.as_dict()), 201

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserListResource, '/users')

# Course Resources
class CourseResource(Resource):
    def get(self, course_id):
        course = Course.query.get(course_id)
        if course:
            return jsonify(course.as_dict())
        return {'message': 'Course not found'}, 404

    def put(self, course_id):
        course = Course.query.get(course_id)
        if course:
            data = request.get_json()
            course.title = data['title']
            course.description = data['description']
            course.category = data['category']
            course.instructor_id = data['instructor_id']
            course.enrollment_limit = data['enrollment_limit']
            db.session.commit()
            return jsonify(course.as_dict())
        return {'message': 'Course not found'}, 404

    def delete(self, course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return {'message': 'Course deleted'}
        return {'message': 'Course not found'}, 404

class CourseListResource(Resource):
    def get(self):
        courses = Course.query.all()
        return jsonify([course.as_dict() for course in courses])

    def post(self):
        data = request.get_json()
        title = data['title']
        description = data['description']
        category = data['category']
        instructor_id = data['instructor_id']
        enrollment_limit = data.get('enrollment_limit')
        course = Course(title=title, description=description, category=category, instructor_id=instructor_id, enrollment_limit=enrollment_limit)
        db.session.add(course)
        db.session.commit()
        return jsonify(course.as_dict()), 201

api.add_resource(CourseResource, '/courses/<int:course_id>')
api.add_resource(CourseListResource, '/courses')

# Enrollment Resources
class EnrollmentResource(Resource):
    def get(self, enrollment_id):
        enrollment = Enrollment.query.get(enrollment_id)
        if enrollment:
            return jsonify(enrollment.as_dict())
        return {'message': 'Enrollment not found'}, 404

    def put(self, enrollment_id):
        enrollment = Enrollment.query.get(enrollment_id)
        if enrollment:
            data = request.get_json()
            enrollment.user_id = data['user_id']
            enrollment.course_id = data['course_id']
            db.session.commit()
            return jsonify(enrollment.as_dict())
        return {'message': 'Enrollment not found'}, 404

    def delete(self, enrollment_id):
        enrollment = Enrollment.query.get(enrollment_id)
        if enrollment:
            db.session.delete(enrollment)
            db.session.commit()
            return {'message': 'Enrollment deleted'}
        return {'message': 'Enrollment not found'}, 404

class EnrollmentListResource(Resource):
    def get(self):
        enrollments = Enrollment.query.all()
        return jsonify([enrollment.as_dict() for enrollment in enrollments])

    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        course_id = data['course_id']
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return jsonify(enrollment.as_dict()), 201

api.add_resource(EnrollmentResource, '/enrollments/<int:enrollment_id>')
api.add_resource(EnrollmentListResource, '/enrollments')

# CourseContent Resources
class CourseContentResource(Resource):
    def get(self, content_id):
        content = CourseContent.query.get(content_id)
        if content:
            return jsonify(content.as_dict())
        return {'message': 'CourseContent not found'}, 404

    def put(self, content_id):
        content = CourseContent.query.get(content_id)
        if content:
            data = request.get_json()
            content.course_id = data['course_id']
            content.topic = data['topic']
            content.content = data['content']
            db.session.commit()
            return jsonify(content.as_dict())
        return {'message': 'CourseContent not found'}, 404

    def delete(self, content_id):
        content = CourseContent.query.get(content_id)
        if content:
            db.session.delete(content)
            db.session.commit()
            return {'message': 'CourseContent deleted'}
        return {'message': 'CourseContent not found'}, 404

class CourseContentListResource(Resource):
    def get(self):
        contents = CourseContent.query.all()
        return jsonify([content.as_dict() for content in contents])

    def post(self):
        data = request.get_json()
        course_id = data['course_id']
        topic = data['topic']
        content = data['content']
        content = CourseContent(course_id=course_id, topic=topic, content=content)
        db.session.add(content)
        db.session.commit()
        return jsonify(content.as_dict()), 201

api.add_resource(CourseContentResource, '/contents/<int:content_id>')
api.add_resource(CourseContentListResource, '/contents')

if __name__ == '__main__':
    with app.app_context():
     db.create_all()
    app.run(debug=True, port=5555)
