from flask import (
    Blueprint, request, current_app, abort, json
)

from ..utils import (
    generic_error_handler
)

import pycpd
import numpy as np
from pycpd import rigid_registration
import numpy as np

cpd = Blueprint('cpd', __name__)


def rad_to_degree(rad):
    return rad * 180 / np.pi


def extract_angle(rot_mat):
    cos_angle = rot_mat[0][0]

    # Validating the value because algorithm representations
    cos_angle = 1 if cos_angle > 1 else\
        (-1 if cos_angle < -1 else cos_angle)

    return rad_to_degree(np.arccos(cos_angle))


@cpd.route('/cpd', methods=['POST'])
def cpd_interface():
    input_data = request.get_json()
    X = np.array(input_data['X'])
    Y = np.array(input_data['Y'])

    reg = rigid_registration(**{'X': X, 'Y': Y, 'tolerance': 0.00001})
    target_Y, (scale, r_rads, t_vec) = reg.register()

    return current_app.response_class(
        response=json.dumps({
            'translation': t_vec.tolist(),
            'rotation': extract_angle(r_rads),
            'scale': scale
        }),
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
