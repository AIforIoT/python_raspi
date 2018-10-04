#!/bin/sh

export FLASK_APP=app
export FLASK_ENV=$2
flask run $1