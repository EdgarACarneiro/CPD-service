#!/bin/sh
python setup.py install
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run