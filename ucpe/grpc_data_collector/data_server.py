import grpc
from concurrent import futures
import time

import ucpe.grpc_data_collector.data_pb2 as data_pb2
import ucpe.grpc_data_collector.data_pb2_grpc as data_pb2_grpc

import ucpe.grpc_data_collector.get_functions as get_functions
import upce.grpc_data_collector.modify_functions as modify_functions
import bridge
import dpdk

PORT = '50051'


class UCPEDataServicer(data_pb2_grpc.UCPEDataServicer):

    def GetData(self, request, context):
        response = data_pb2.DataResponse()
        if request.command == 'hugepages':
            if request.str_request == 'total':
                response.header = "Total hugepages memory in kB"
                response.int_response = get_functions.get_hugepages_totalmem_kB()
            elif request.str_request == 'free':
                response.header = "Total free hugepages memory in kB"
                response.int_response = get_functions.get_hugepages_freemem_kB()
        elif request.command == 'memory':
            if request.str_request == 'total':
                response.header = "Total memory in kB"
                response.int_response = get_functions.get_total_mem_kB()
            elif request.str_request == 'available':
                response.header = "Total available memory in kB"
                response.int_response = get_functions.get_avail_mem_kB()
        elif request.command == 'cpu':
            if request.str_request == 'total':
                response.header = "Total CPUs"
                response.int_response = get_functions.get_total_cpus()
        elif request.command == 'netifaces':
            if request.str_request == 'list':
                response.header = "List of network interfaces"
                response.str_response = str(get_functions.get_network_interfaces())
        elif request.command == 'bridge':
            if request.str_request == 'list':
                response.header = "List of Linux bridges"
                response.str_response = str(get_functions.print_linux_bridges_list())
            elif request.str_request == 'all':
                response.header = "All Linux bridge info"
                response.str_response = str(get_functions.get_linux_bridges_all())
            elif request.str_request == 'details':
                response.header = f'Details for {request.str_param1}'
                response.str_response = str(get_functions.get_linux_bridge_details(request.str_param1))
        elif request.command == 'dpdk':
            if request.str_request == 'devices':
                response.header = "List of network devices using DPDK-compatible drivers"
                response.str_response = str(get_functions.dpdk_get_devices())

        return response

    def ModifyData(self, request, context):
        response = data_pb2.DataChangeResponse()
        if request.command == 'dpdk':
            if request.str_request == 'bind':
                response.response = f"Binding {request.str_param1} to {request.str_param2}, please wait"
                p = modify_functions.dpdk_bind(request.str_param1, request.str_param2)
                response.status = True
                return p

            elif request.str_request == 'unbind':
                response.response = f"Unbinding {request.str_param1}, please wait"
                p = modify_functions.dpdk_unbind(request.str_param1)
                response.status = True
                return p

            elif request.str_request == 'enable':
                response.response = f"Enabling {request.str_param1} driver, please wait"
                p = modify_functions.dpdk_enable(request.str_param1)
                response.status = True
                return p

            elif request.str_request == 'add_port':
                response.response = f"Adding {request.str_param2} to bridge {request.str_param1}, please wait"
                p = modify_functions.dpdk_add_port(request.str_param1, request.str_param2, request.str_param3)
                response.status = True
                return p


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

data_pb2_grpc.add_UCPEDataServicer_to_server(UCPEDataServicer(), server)

print(f'Starting server. Listening on port {PORT}')
server.add_insecure_port(f'[::]:{PORT}')

server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
