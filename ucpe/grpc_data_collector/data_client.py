import grpc

import ucpe.grpc_data_collector.data_pb2 as data_pb2
import ucpe.grpc_data_collector.data_pb2_grpc as data_pb2_grpc

HOSTNAME = '10.10.81.100'
PORT = '50051'


def run(request_type, hostname=HOSTNAME, port=PORT, str_param1=None, str_param2=None, str_param3=None, str_param4=None,
        str_param5='', **kwargs):

    if 'hostname' in kwargs['body']:
        hostname = kwargs['body']['hostname']
    if 'port' in kwargs['body']:
        port = kwargs['body']['port']
    command = kwargs['body']['command']
    str_request = kwargs['body']['str_request']
    if 'str_param1' in kwargs['body']:
        str_param1 = kwargs['body']['str_param1']
    if 'str_param2' in kwargs['body']:
        str_param2 = kwargs['body']['str_param2']
    if 'str_param3' in kwargs['body']:
        str_param3 = kwargs['body']['str_param3']
    if 'str_param4' in kwargs['body']:
        str_param4 = kwargs['body']['str_param4']
    if 'str_param5' in kwargs['body']:
        str_param5 = kwargs['body']['str_param5']

    channel = grpc.insecure_channel(f'{hostname}:{port}')
    stub = data_pb2_grpc.UCPEDataStub(channel)
    requested = data_pb2.DataRequest(command=f'{command}', str_request=f'{str_request}', str_param1=f'{str_param1}',
                                     str_param2=f'{str_param2}', str_param3=f'{str_param3}', str_param4=f'{str_param4}',
                                     str_param5=f'{str_param5}')

    print(requested)
    response = None

    if request_type == 'get':
        response = stub.GetData(requested)

    elif request_type == 'modify':
        response = stub.ModifyData(requested)
    return response


def main(response_type, **kwargs):
    response = run(response_type, **kwargs)
    print(response)


if __name__ == "__main__":
    request = 'get'
    kwargs = {'body': {'command': 'sriov', 'str_request': 'num_vfs', 'str_param1': 'b7:00.3'}}
    # print(kwargs['body']['str_param1'])
    main(request, **kwargs)
