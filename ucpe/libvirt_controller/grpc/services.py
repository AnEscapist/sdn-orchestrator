import ucpe.libvirt_controller.grpc.libvirt_pb2 as libvirt_pb2
import ucpe.libvirt_controller.grpc.libvirt_pb2_grpc as libvirt_pb2_grpc
from ucpe.libvirt_controller.grpc.blockpull import blockpull

class LibvirtServicer(libvirt_pb2_grpc.LibvirtServicer):

    def BlockPull(self, request, context):
        response = libvirt_pb2.Response()
        blockpull(request.domain, request.path, request.base)
        response.success = "hi"
