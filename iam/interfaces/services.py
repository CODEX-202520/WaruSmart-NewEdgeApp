from flask import request, jsonify, Blueprint

from iam.application.services import AuthApplicationService

iam_api: Blueprint = Blueprint('iam_api', __name__)
auth_service = AuthApplicationService()

def authenticate_request():
    device_id = request.json.get("device_id") if request.json else None
    api_key = request.headers.get("X-API-Key")
    if not device_id or not api_key:
        return jsonify({"error": "No device id or API key provided"}), 401
    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid API key provided"}), 401
    return None
