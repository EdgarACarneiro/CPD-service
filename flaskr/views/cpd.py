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
    degree = rad_to_degree(np.arccos(cos_angle))

    # Check degree signal
    return degree if rot_mat[0][1] > 0 else degree * -1


def extract_rigid(cpd_res):
    _, (scale, r_rads, t_vec) = cpd_res
    return {
        'translation': t_vec.tolist(),
        'rotation': extract_angle(r_rads),
        'scale': scale
    }


def run_CPD(input_data):
    '''Run the CPD algorithm and return the identified object'''

    try:
        X = np.array(input_data['X'] if 'X' in input_data else input_data['x'])
        Y = np.array(input_data['Y'] if 'Y' in input_data else input_data['y'])
    except:
        abort(404)

    reg = rigid_registration(**{'X': Y, 'Y': X, 'tolerance': 0.00001})
    return reg.register()


@cpd.route('/cpd', methods=['POST'])
def cpd_interface():
    return current_app.response_class(
        response=json.dumps(
            extract_rigid(
                run_CPD(request.get_json()))),
        status=200,
        mimetype='application/json'
    )


@cpd.route('/cpd-all', methods=['POST'])
def cpd_all():
    res = []
    for phenomenon in request.get_json():
        res.append(
            extract_rigid(
                run_CPD(phenomenon)))

    return current_app.response_class(
        response=json.dumps({'transformations': res}),
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
