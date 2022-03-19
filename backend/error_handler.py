from flask import jsonify
from setup import app

@app.errorhandler(404)
def not_found(error):
    # if request.path.startswith("/api/"):
    return jsonify({
        'status': 'fail',
        'message': f'{str(error)} Not Found'
    }), 404
    # return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'status': 'fail',
        'message': f'Unprocessable {str(error)}'
    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'status': 'fail',
        'message': 'Bad Request'
    }), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'status': 'fail',
        'message': 'Your password is not correct.'
    }), 401

@app.errorhandler(500)
def sever_error(error):
    return jsonify({
        'status': 'fail',
        'message': f'Sever Error: {str(error)}'
    }), 500