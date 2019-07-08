import grpc
from concurrent import futures
import time

import ucpe.libvirt_controller.grpc.libvirt_pb2 as libvirt_pb2
import ucpe.libvirt_controller.grpc.libvirt_pb2_grpc as libvirt_pb2_grpc
from ucpe.libvirt_controller.grpc.services import LibvirtServicer
import sys
sys.path.append('/home/attadmin/projects/sdn-orchestrator/')

MAX_WORKERS = 10
server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))

libvirt_pb2_grpc.add_LibvirtServicer_to_server(LibvirtServicer(), server)

print('Starting server, listening on port 50061')
server.add_insecure_port('[::]:50061')
server.start()

try:
    while True:
        time.sleep(86400)

except KeyboardInterrupt:
    server.stop(0)

