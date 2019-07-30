import grpc
from concurrent import futures
import time
import sys
import json

sys.path.append('/home/potato/projects/sdn-orchestrator/')

import ucpe.grpc_data_collector.data_pb2 as data_pb2
import ucpe.grpc_data_collector.data_pb2_grpc as data_pb2_grpc

import ucpe.grpc_data_collector.get_functions as get_functions
import ucpe.grpc_data_collector.modify_functions as modify_functions
# import bridge
# import dpdk

PORT = '50051'


class UCPEDataServicer(data_pb2_grpc.UCPEDataServicer):

    def GetData(self, request, context):
        response = data_pb2.DataResponse()
        # print('hello')
        if request.command == 'hugepages':
            if request.str_request == 'total':
                response.header = "Total hugepages memory"
                response.str_response = get_functions.get_hugepages_totalmem()
            elif request.str_request == 'free':
                response.header = "Total free hugepages memory"
                response.str_response = get_functions.get_hugepages_freemem()
            elif request.str_request == 'free_b':
                response.header = "Total free hugepages memory in bytes"
                response.str_response = get_functions.get_hugepages_freemem_b()

        elif request.command == 'memory':
            if request.str_request == 'total':
                response.header = "Total memory"
                response.str_response = get_functions.get_total_mem()
            elif request.str_request == 'available':
                response.header = "Total available memory"
                response.str_response = get_functions.get_avail_mem()
            elif request.str_request == 'available_b':
                response.header = "Total available memory in bytes"
                response.str_response = get_functions.get_avail_mem_b()

        elif request.command == 'cpu':
            if request.str_request == 'total':
                response.header = "Total CPUs"
                response.str_response = str(get_functions.get_total_cpus())

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
                response.str_response = json.dumps(get_functions.dpdk_get_devices())

        elif request.command == 'sriov':
            if request.str_request == 'total_vfs':
                response.header = f"Total vfs for {request.str_param1}"
                response.str_response = get_functions.sriov_totalvfs(request.str_param1)
            elif request.str_request == 'num_vfs':
                response.header = f'Current vfs for {request.str_param1}'
                response.str_response = get_functions.sriov_numvfs(request.str_param1)
        return response

# ==============================================================================================

    def ModifyData(self, request, context):
        response = data_pb2.DataChangeResponse()

        if request.command == 'sriov':
            None

        elif request.command == 'dpdk':
            if request.str_request == 'bind':
                # print('trying to bind')
                response.status = f'Binding {request.str_param1} to {request.str_param2}, please wait'
                print(response.status)
                proc = modify_functions.dpdk_bind(request.str_param1, request.str_param2, force=True)
                if proc:
                    response.status = f'Binding {request.str_param1} to {request.str_param2} successful'
                else:
                    response.status = f'Binding {request.str_param1} to {request.str_param2} unsuccessful'
                response.str_response = json.dumps(get_functions.dpdk_get_devices())
                print(response.status)

            elif request.str_request == 'unbind':
                response.status = f'Unbinding {request.str_param1}, please wait'
                print(response.status)
                proc = modify_functions.dpdk_unbind(request.str_param1)
                if proc:
                    response.status = f'Unbinding {request.str_param1} successful'
                else:
                    response.status = f'Unbinding {request.str_param1} unsuccessful'
                response.str_response = json.dumps(get_functions.dpdk_get_devices())
                print('Unbind successful')

            elif request.str_request == 'enable':
                response.status = f'Enabling {request.str_param1} driver, please wait'
                print(response.str_response)
                proc = modify_functions.dpdk_enable(request.str_param1)
                if proc:
                    response.status = f'Enabling {request.str_param1} successful'
                else:
                    response.status = f'Enabling {request.str_param1} unsuccessful'
                print('Driver enabled')

        elif request.command == 'ovs':
            if request.str_request == 'add_port':
                response.status = f"Adding {request.str_param2} to bridge {request.str_param1}, please wait"
                print(response.str_response)
                proc = modify_functions.ovs_add_port(request.str_param1, request.str_param2,
                                                     request.str_param3, request.str_param4)
                if proc:
                    response.status = f"Port {request.str_param2} added"
                response.str_response = str(get_functions.ovs_list_ports(request.str_param1))

            elif request.str_request == 'del_port':
                response.status = f"Deleting all ports connected to {request.str_param1} from {request.str_param2}, " \
                                  f"please wait"
                print(response.status)
                proc = modify_functions.ovs_del_port(request.str_param1, request.str_param2)
                if proc:
                    # print(response.str_response)
                    response.status = "Deletion successful"
                else:
                    response.status = "Deletion unsuccessful"
                response.str_response = str(get_functions.ovs_list_ports(request.str_param1))

        elif request.command == 'ovs_docker':
            if request.str_request == 'add_port':
                response.status = f"Adding {request.str_param2} inside {request.str_param3} and " \
                    f"connecting to bridge {request.str_param1} via {request.str_param4}"
                print(response.status)
                proc = modify_functions.ovs_docker_add_port(request.str_param1, request.str_param2, request.str_param3,
                                                            request.str_param4, request.str_param5, request.str_param6)
                if proc[0]:
                    response.status = f'Interface {request.str_param2} added'
                else:
                    response.status = f'Request failed'
                if request.str_param4 != str(proc[1]):
                    response.str_response = f"Using port {str(proc[1])}"
                else:
                    response.str_response = f"Using port {request.str_param4}"

            elif request.str_request == 'del_port':
                response.status = f"Deleting all ports connected to {request.str_param1} from {request.str_param2}," \
                                  f" please wait"
                print(response.status)
                proc = modify_functions.ovs_docker_del_port(request.str_param1, request.str_param2)
                if proc:
                    # print(response.str_response)
                    response.status = "Deletion successful"
                else:
                    response.status = "Deletion unsuccessful"
                response.str_response = str(get_functions.ovs_list_ports(request.str_param1))
        return response


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
