#!/bin/sh

export FLASK_APP=$3
export FLASK_ENV=$2
#source $(pipenv --venv)/bin/activate
flask run $1
