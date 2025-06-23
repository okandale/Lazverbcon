from flask import abort, Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import os

admin = Blueprint("admin", __name__)

@admin.route("/auth", methods=["POST"])
def auth():
    """Authenticate the user."""
    username = request.json.get("username")
    password = request.json.get("password")
    
    if username is None or password is None:
        abort(400)
    
    if username == "admin" and password == os.environ.get("ADMIN_PASSWORD"):
        # Okay.
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token})
    else:
        abort(401)  # Not okay.


@admin.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@admin.route("/me")
@jwt_required()
def me():
    """A simple, protected route to detect whether we are authenticated."""
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200