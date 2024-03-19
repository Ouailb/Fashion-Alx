#!/usr/bin/python3
""" My Api """
from models import storage
from api.views.__init__ import app_views
from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
app.config["SECRET_KEY"] = "1Edm+wbB8dYfIWhekEOGUI0(-fCsqwLO"
app.config["JWT_SECRET_KEY"] = "+nW%IuM@0%DQ@T94&(untLGmyPYTU3gz"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not Found"}), 404)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
