from flask import (
    Blueprint, request, current_app, request, abort, json
)

from ..utils import (
    generic_error_handler
)

import pycpd

cpd = Blueprint('cpd', __name__)


@cpd.route('/cpd', methods=['POST'])
def cpd_interface():
    input_data = request.get_json()


    return current_app.response_class(
        response=json.dumps(input_data),
        status=200,
        mimetype='application/json'
    )

# Customized Error handlers
@cpd.errorhandler(401)
def handle_unauthorized_request(e):
    return generic_error_handler(
        401, "Attempt of unauthorized access to information."
    )


@cpd.errorhandler(400)
def handle_bad_request(e):
    return generic_error_handler(
        400, "Invalid data passed in request"
    )
