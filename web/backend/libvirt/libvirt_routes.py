from flask import Blueprint, render_template, abort,jsonify
from jinja2 import TemplateNotFound

libvirt_routes = Blueprint('libvirt_page', __name__, template_folder='templates')

@libvirt_routes.route('/libvirt/hello')
def hello():
    return jsonify(name='zhengqi')
