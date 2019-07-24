# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import ucpe.bcm_controller.grpc.autobcm_pb2 as autobcm__pb2


class AutoBCMStub(object):
  """define the service
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ShowActivePorts = channel.unary_unary(
        '/autobcm.AutoBCM/ShowActivePorts',
        request_serializer=autobcm__pb2.ConfigRequest.SerializeToString,
        response_deserializer=autobcm__pb2.ConfigReply.FromString,
        )
    self.CreateVLAN = channel.unary_unary(
        '/autobcm.AutoBCM/CreateVLAN',
        request_serializer=autobcm__pb2.ConfigRequest.SerializeToString,
        response_deserializer=autobcm__pb2.ConfigReply.FromString,
        )
    self.AddPorts = channel.unary_unary(
        '/autobcm.AutoBCM/AddPorts',
        request_serializer=autobcm__pb2.ConfigRequest.SerializeToString,
        response_deserializer=autobcm__pb2.ConfigReply.FromString,
        )
    self.SetPVLAN = channel.unary_unary(
        '/autobcm.AutoBCM/SetPVLAN',
        request_serializer=autobcm__pb2.ConfigRequest.SerializeToString,
        response_deserializer=autobcm__pb2.ConfigReply.FromString,
        )
    self.ShowVLANs = channel.unary_unary(
        '/autobcm.AutoBCM/ShowVLANs',
        request_serializer=autobcm__pb2.ConfigRequest.SerializeToString,
        response_deserializer=autobcm__pb2.ConfigReply.FromString,
        )
    self.DestroyVLAN = channel.unary_unary(
        '/autobcm.AutoBCM/DestroyVLAN',
        request_serializer=autobcm__pb2.ConfigRequest.SerializeToString,
        response_deserializer=autobcm__pb2.ConfigReply.FromString,
        )
    self.RemovePorts = channel.unary_unary(
        '/autobcm.AutoBCM/RemovePorts',
        request_serializer=autobcm__pb2.ConfigRequest.SerializeToString,
        response_deserializer=autobcm__pb2.ConfigReply.FromString,
        )
    self.ShowPVLANs = channel.unary_unary(
        '/autobcm.AutoBCM/ShowPVLANs',
        request_serializer=autobcm__pb2.ConfigRequest.SerializeToString,
        response_deserializer=autobcm__pb2.ConfigReply.FromString,
        )


class AutoBCMServicer(object):
  """define the service
  """

  def ShowActivePorts(self, request, context):
    """Configure the Broadcom Shell
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateVLAN(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddPorts(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetPVLAN(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ShowVLANs(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DestroyVLAN(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemovePorts(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ShowPVLANs(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_AutoBCMServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ShowActivePorts': grpc.unary_unary_rpc_method_handler(
          servicer.ShowActivePorts,
          request_deserializer=autobcm__pb2.ConfigRequest.FromString,
          response_serializer=autobcm__pb2.ConfigReply.SerializeToString,
      ),
      'CreateVLAN': grpc.unary_unary_rpc_method_handler(
          servicer.CreateVLAN,
          request_deserializer=autobcm__pb2.ConfigRequest.FromString,
          response_serializer=autobcm__pb2.ConfigReply.SerializeToString,
      ),
      'AddPorts': grpc.unary_unary_rpc_method_handler(
          servicer.AddPorts,
          request_deserializer=autobcm__pb2.ConfigRequest.FromString,
          response_serializer=autobcm__pb2.ConfigReply.SerializeToString,
      ),
      'SetPVLAN': grpc.unary_unary_rpc_method_handler(
          servicer.SetPVLAN,
          request_deserializer=autobcm__pb2.ConfigRequest.FromString,
          response_serializer=autobcm__pb2.ConfigReply.SerializeToString,
      ),
      'ShowVLANs': grpc.unary_unary_rpc_method_handler(
          servicer.ShowVLANs,
          request_deserializer=autobcm__pb2.ConfigRequest.FromString,
          response_serializer=autobcm__pb2.ConfigReply.SerializeToString,
      ),
      'DestroyVLAN': grpc.unary_unary_rpc_method_handler(
          servicer.DestroyVLAN,
          request_deserializer=autobcm__pb2.ConfigRequest.FromString,
          response_serializer=autobcm__pb2.ConfigReply.SerializeToString,
      ),
      'RemovePorts': grpc.unary_unary_rpc_method_handler(
          servicer.RemovePorts,
          request_deserializer=autobcm__pb2.ConfigRequest.FromString,
          response_serializer=autobcm__pb2.ConfigReply.SerializeToString,
      ),
      'ShowPVLANs': grpc.unary_unary_rpc_method_handler(
          servicer.ShowPVLANs,
          request_deserializer=autobcm__pb2.ConfigRequest.FromString,
          response_serializer=autobcm__pb2.ConfigReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'autobcm.AutoBCM', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
