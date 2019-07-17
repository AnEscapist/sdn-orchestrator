from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function

grpc_routes = Blueprint('grpc', __name__, template_folder='templates')

@app.route('/'
