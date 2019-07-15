import sys
sys.path.append('/home/attadmin/projects/sdn-orchestrator/')
sys.path.append('/home/att-pc-7/Zhengqi/Project/sdn-orchestrator/')
sys.path.append('/home/att/projects/sdn-orchestrator/')
from flask import Flask, escape, request, jsonify
from web.backend.libvirt.libvirt_routes import libvirt_routes
from web.backend.docker.docker_routes import docker_routes
from web.backend.grpc_data_collector.grpc_routes import grpc_routes
import web.backend.zmq_web as zmq_web

app = Flask(__name__)
app.register_blueprint(libvirt_routes)
app.register_blueprint(docker_routes)
app.register_blueprint(grpc_routes)

def serve():
    zmq_web.start()
    app.run(threaded=True)

if __name__ == "__main__":
    serve()
