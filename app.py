from flask import Flask

import iam.application.services
from iam.interfaces.services import iam_api
from monitoring.interfaces.actuator import actuator_api
from monitoring.interfaces.services import monitoring_api  # importa tu blueprint de métricas
from shared.infrastructure.database import init_db

app = Flask(__name__)

app.register_blueprint(iam_api)
app.register_blueprint(monitoring_api)  # registra el blueprint de métricas

app.register_blueprint(actuator_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()
        auth_application_service = iam.application.services.AuthApplicationService()
        auth_application_service.get_or_create_test_device()

if __name__ == '__main__':
    app.run(debug=True, host='192.168.244.109', port=5000)