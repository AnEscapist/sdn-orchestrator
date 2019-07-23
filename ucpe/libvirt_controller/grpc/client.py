import grpc
import ucpe.libvirt_controller.grpc.libvirt_pb2 as libvirt_pb2
import ucpe.libvirt_controller.grpc.libvirt_pb2_grpc as libvirt_pb2_grpc

# channel = grpc.insecure_channel('10.10.81.100:50061')
# stub = libvirt_pb2_grpc.LibvirtStub(channel)
# request = libvirt_pb2.BlockPullRequest(domain="test", path="/home/potato/libvirt/backups/snap2.qcow2",
#                                        base="/var/third-party/ubuntu_16_roger.qcow2")
# response = stub.BlockPull(request)
#
# print(response.out)
# print(response.error)

channel = grpc.insecure_channel('10.10.81.100:50061')
stub = libvirt_pb2_grpc.LibvirtStub(channel)
request = libvirt_pb2.CopyRequest(vm_name="test", image_file_name="storage.qcow2")
response = stub.CopyRequest(request)

print(response.out)
print(response.error)
