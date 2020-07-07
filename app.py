import os
from flask import Flask
from flask import render_template
from balena import Balena
from dotenv import load_dotenv

load_dotenv()
balena = Balena()

auth_token = os.getenv("AUTH_TOKEN")
app_id = os.getenv("APP_ID")

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/disable')
def enable():
    return create_fleet_variable()

@app.route('/enable')
def disable():
    return delete_fleet_variable()

def get_variable_id():
    variables = balena.models.environment_variables.application.get_all(app_id)
    for i in variables:
        if i['name'] == 'DISABLE_MULTI_ROOM':
            return i['id']

    return None

def create_fleet_variable():
    balena.auth.login_with_token(auth_token)
    variable_id = get_variable_id()
    if variable_id is None:
        response = balena.models.environment_variables.application.create(app_id, 'DISABLE_MULTI_ROOM', '1')
        return response
    return "No need to add"

def delete_fleet_variable():
    balena.auth.login_with_token(auth_token)
    variable_id = get_variable_id()
    if variable_id is not None:
        response = balena.models.environment_variables.application.remove(get_variable_id())
        return response

    return "No need to delete"
