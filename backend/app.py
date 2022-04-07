import os
from flask import send_from_directory
from setup import app

## Blueprint Imports
from api.auth import auth
from api.users import user
from api.section import section
from api.education import education
from api.sub_education import sub_education
# from api.classes import classes
# from api.exams import exams
# from api.level import level
from api.speciality import specialty
# from api.subject import subject
# from api.resources import resource
# from api.student import student
from api.teacher import teacher
# from api.newses import news




@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                            'GET, PUT, POST, PATCH, DELETE, OPTIONS')
    return response

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def index(path):
#     print(path)
#     path_dir = os.path.abspath("../frontend/build") #path react build
#     if path != "" and os.path.exists(os.path.join(path_dir, path)):
#         return send_from_directory(os.path.join(path_dir), path)
#     return send_from_directory(app.static_folder, 'index.html')

### Register blueprints
app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(section)
app.register_blueprint(education)
app.register_blueprint(sub_education)
# app.register_blueprint(classes)
# app.register_blueprint(exams)
# app.register_blueprint(level)
app.register_blueprint(specialty)
# app.register_blueprint(subject)
# app.register_blueprint(resource)
app.register_blueprint(teacher)
# app.register_blueprint(student)
# app.register_blueprint(news)


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)