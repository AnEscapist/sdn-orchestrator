from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound

grpc_routes = Blueprint('page', __name__, template_folder='templates')

@grpc_routes.route('/data-collect/dashboard')
def hello():
    return jsonify(name='zhengqi')