from flask import Blueprint, render_template, abort,jsonify
from jinja2 import TemplateNotFound

docker_routes = Blueprint('docker_page', __name__, template_folder='templates')

@docker_routes.route('/docker/hello')
def hello():
    return jsonify(name='docker docker')
