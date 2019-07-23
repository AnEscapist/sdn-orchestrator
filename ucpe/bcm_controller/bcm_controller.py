
from inspect import signature, Parameter

from ucpe.bcm_controller.utils import get_caller_function_name

import ucpe.bcm_controller.grpc.autobcm_pb2 as autobcm_pb2
import ucpe.bcm_controller.grpc.autobcm_pb2_grpc as autobcm_pb2_grpc

import grpc

hostname = "10.10.81.250:50051"

class BCMController:

    @staticmethod
    def bcm_controller_create_vlan(**kwargs):
        func = create_vlan
        return _call_function(func, **kwargs)

    @staticmethod
    def bcm_controller_destroy_vlan(**kwargs):
        func = destroy_vlan
        return _call_function(func, **kwargs)

    @staticmethod
    def bcm_controller_show_vlans(**kwargs):
        func = show_vlans
        return _call_function(func, **kwargs)

    @staticmethod
    def bcm_controller_add_ports(**kwargs):
        func = add_ports
        return _call_function(func, **kwargs)

    @staticmethod
    def bcm_controller_rem_ports(**kwargs):
        func = rem_ports
        return _call_function(func, **kwargs)

    @staticmethod
    def bcm_controller_set_pvlan(**kwargs):
        func = set_pvlan
        return _call_function(func, **kwargs)

    @staticmethod
    def bcm_controller_show_pvlans(**kwargs):
        func = show_pvlans
        return _call_function(func, **kwargs)


def create_vlan(vlanid, pbm='', ubm=''):
    channel = grpc.insecure_channel(hostname)
    stub = autobcm_pb2_grpc.AutoBCMStub(channel)
    request = autobcm_pb2.ConfigRequest(vlanid=vlanid, pbm=pbm, ubm=ubm)
    rv = ''
    response = stub.CreateVLAN(request)
    rv = rv + response.message
    if pbm != '':
        response = stub.AddPorts(request)
        rv = rv + '\n' + response.message
    return rv


def destroy_vlan(vlanid):
    channel = grpc.insecure_channel(hostname)
    stub = autobcm_pb2_grpc.AutoBCMStub(channel)
    request = autobcm_pb2.ConfigRequest(vlanid=vlanid)
    response = stub.DestroyVLAN(request)
    return response.message


def show_vlans():
    channel = grpc.insecure_channel(hostname)
    stub = autobcm_pb2_grpc.AutoBCMStub(channel)
    request = autobcm_pb2.ConfigRequest()
    response = stub.ShowVLANs(request)
    return response.message


def add_ports(vlanid, pbm, ubm=''):
    channel = grpc.insecure_channel(hostname)
    stub = autobcm_pb2_grpc.AutoBCMStub(channel)
    request = autobcm_pb2.ConfigRequest(vlanid=vlanid, pbm=pbm, ubm=ubm)
    response = stub.AddPorts(request)
    return response.message


def rem_ports(vlanid, pbm):
    channel = grpc.insecure_channel(hostname)
    stub = autobcm_pb2_grpc.AutoBCMStub(channel)
    request = autobcm_pb2.ConfigRequest(vlanid=vlanid, pbm=pbm)
    response = stub.RemovePorts(request)
    return response.message


def set_pvlan(vlanid, pbm):
    channel = grpc.insecure_channel(hostname)
    stub = autobcm_pb2_grpc.AutoBCMStub(channel)
    request = autobcm_pb2.ConfigRequest(vlanid=vlanid, pbm=pbm)
    response = stub.SetPVLAN(request)
    return response.message


def show_pvlans():
    channel = grpc.insecure_channel(hostname)
    stub = autobcm_pb2_grpc.AutoBCMStub(channel)
    request = autobcm_pb2.ConfigRequest()
    response = stub.ShowPVLANs(request)
    return response.message


def _call_function(func, **kwargs):
    body = kwargs["body"]  # todo: bad
    params = signature(func).parameters  # get the function arguments
    relevant_kwargs = {}  # todo: this is REALLY bad
    for param in params:
        if params[param].default == Parameter.empty:
            try:
                relevant_kwargs[param] = body[param]
            except KeyError:
                raise KeyError("missing argument " + param + " in call to " + func.__name__)
        else:  # todo: this is REALLY bad - depends on the arg name, but so does the request/response
            relevant_kwargs[param] = body.get(param, params[param].default)
    return_dict = {}
    return_dict["result"] = func(**relevant_kwargs)
    caller_name = get_caller_function_name()
    return_dict["function"] = caller_name
    return return_dict
