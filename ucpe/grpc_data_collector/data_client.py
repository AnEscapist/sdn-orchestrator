import grpc

import data_pb2
import data_pb2_grpc

HOSTNAME = '10.10.81.100'
PORT = '50051'


def run(request_type, hostname=HOSTNAME, port=PORT, str_param1=None, str_param2=None, str_param3=None, **kwargs):
    if 'hostname' in kwargs:
        hostname = kwargs['body']['hostname']
    if 'port' in kwargs:
        port = kwargs['body']['port']
    command = kwargs['body']['command']
    str_request = kwargs['body']['str_request']
    if 'str_param1' in kwargs:
        str_param1 = kwargs['body']['str_param1']
    if 'str_param2' in kwargs:
        str_param2 = kwargs['body']['str_param2']
    if 'str_param3' in kwargs:
        str_param3 = kwargs['body']['str_param3']

    channel = grpc.insecure_channel(f'{hostname}:{port}')
    stub = data_pb2_grpc.UCPEDataStub(channel)
    request = data_pb2.DataRequest(command=f'{command}', str_request=f'{str_request}', str_param1=f'{str_param1}',
                                   str_param2=f'{str_param2}', str_param3=f'{str_param3}')
    response = None
    if request_type == 'modify':
        response = stub.ModifyData(request)
    if request_type == 'get':
        response = stub.GetData(request)

    return response


def main(response_type, **kwargs):
    response = run(response_type, **kwargs)
    print(response)


if __name__ == "__main__":
    request = 'get'
    kwargs = {'body': {'hostname': '10.10.81.100', 'port': '50051', 'command': 'bridge', 'str_request': 'list'}}
    main(request, **kwargs)
