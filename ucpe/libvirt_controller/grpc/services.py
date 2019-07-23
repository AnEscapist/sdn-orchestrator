import ucpe.libvirt_controller.grpc.libvirt_pb2 as libvirt_pb2
import ucpe.libvirt_controller.grpc.libvirt_pb2_grpc as libvirt_pb2_grpc
from ucpe.libvirt_controller.grpc.blockpull import blockpull
from ucpe.libvirt_controller.grpc.copy_image import copy_image

class LibvirtServicer(libvirt_pb2_grpc.LibvirtServicer):

    def BlockPull(self, request, context):
        response = libvirt_pb2.Response()
        out,err = blockpull(request.domain, request.path, request.base)
        response.out = out
        response.error = err
        return response

    def CopyImage(self, request, context):
        response = libvirt_pb2.Response()
        out,err = copy_image(request.vm_name, request.image_file_name)
        response.out = out
        response.error = err
        return response

