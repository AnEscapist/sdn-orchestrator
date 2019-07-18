from flask import Blueprint, render_template, abort,jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function

vm_routes = Blueprint('libvirt', __name__)

@vm_routes.route('/libvirt/hello')
def hello():
    return jsonify(name='zhengqi')
