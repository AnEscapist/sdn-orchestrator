import sys
sys.path.append('/home/attadmin/projects/sdn-orchestrator/')
sys.path.append('/home/att-pc-7/Zhengqi/Project/sdn-orchestrator/')
sys.path.append('/home/att/projects/sdn-orchestrator/')
sys.path.append('/home/allen/sdn-orchestrator/')
from flask import Flask, escape, request, jsonify
from web.backend.utils.util_routes import util_routes
from web.backend.vms.vm_routes import vm_routes
from web.backend.docker.docker_routes import docker_routes
from web.backend.grpc.grpc_routes import grpc_routes
from web.backend.bcm.bcm_routes import bcm_routes
import web.backend.zmq_web as zmq_web

app = Flask(__name__)
app.register_blueprint(util_routes, url_prefix='/utils')
app.register_blueprint(vm_routes, url_prefix='/vms')
app.register_blueprint(docker_routes)
app.register_blueprint(grpc_routes)
app.register_blueprint(bcm_routes, url_prefix='/bcm')

def serve():
    zmq_web.start()
    app.run(threaded=True, host='0.0.0.0') # each request in its own thread, host=0.0.0.0 is so server can run on a different computer from frontend

if __name__ == "__main__":
    serve()
