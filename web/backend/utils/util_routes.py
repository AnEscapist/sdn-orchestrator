from flask import Blueprint, request, render_template, abort, jsonify
from jinja2 import TemplateNotFound
from web.backend.zmq_web import call_ucpe_function
import os
import socket

util_routes = Blueprint('utils', __name__)

@util_routes.route('/ipv4')
def utils_get_ipv4():
    ipv4 = socket.gethostbyname(socket.getfqdn())
    return jsonify(ipv4=ipv4)
