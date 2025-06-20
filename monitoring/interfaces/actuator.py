# actuator.py (En monitoring/interfaces/actuator.py)
from flask import Flask, Blueprint, request, jsonify

actuator_api = Blueprint('actuator_api', __name__)

# Tu código Flask aquí
@actuator_api.route('/api/v1/actuators/status', methods=['GET'])
def get_activation_status():
    # Código para manejar la solicitud GET
    return jsonify({"status": "success"})

def create_app():
    app = Flask(__name__)
    app.register_blueprint(actuator_api)  # Registra el blueprint
    return app
