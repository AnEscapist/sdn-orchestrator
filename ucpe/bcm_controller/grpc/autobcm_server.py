# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import time
import logging

import grpc
import pexpect
import bcmutils
#import ovsutils

import autobcm_pb2
import autobcm_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
bcm=None

class AutoBCM(autobcm_pb2_grpc.AutoBCMServicer):
    def CreateVLAN(self, request, context):
        bcmutils.create_vlan(bcm,request.vlanid)
        return autobcm_pb2.ConfigReply(message='Created VLAN ' + str(request.vlanid))
    def AddPorts(self, request, context):
        bcmutils.add_ports(bcm,request.vlanid,request.pbm,request.ubm)
        return autobcm_pb2.ConfigReply(message='Added ports to VLAN ' + str(request.vlanid))
    def SetPVLAN(self, request, context):
        bcmutils.set_pvlan(bcm,request.pbm,vlanid)
        return autobcm_pb2.ConfigReply(message='Set default VLAN of port(s) ' + str(request.pbm) + ' to VLAN ' + str(request.vlanid))
    def ShowVLANs(self, request, context):
        return autobcm_pb2.ConfigReply(message=bcmutils.show_vlans(bcm))
    def DestroyVLAN(self, request, context):
        bcmutils.destroy_vlan(bcm,request.vlanid)
        return autobcm_pb2.ConfigReply(message='Destroyed VLAN ' + str(request.vlanid))
    def RemovePorts(self, request, context):
        bcmutils.rem_ports(bcm,request.vlanid,request.pbm)
        return autobcm_pb2.ConfigReply(message='Removed ports from VLAN ' + str(request.vlanid))
    def ShowPVLANs(self, request, context):
        return autobcm_pb2.ConfigReply(message=bcumutils.show_pvlans(bcm))

    #def ConfigBCM(self, request, context):	
        #call the functions defined in the helper utils to config BCM. These are all hard-coded but you can modify them to take inputs from the user or elsewhere if you wish.
        #bcmutils.create_vlan(bcm,100)
        #bcmutils.create_vlan(bcm,302)
        #bcmutils.add_ports(bcm,100,'ge4,xe8','ge4')
        #bcmutils.add_ports(bcm,302,'ge9,xe9','ge9')
        #bcmutils.set_pvlan(bcm,'ge4',100)
        #bcmutils.set_pvlan(bcm,'ge9',302)
        #return autobcm_pb2.ConfigReply(message='Done setting up BCM VLANs!')
        #return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    global bcm    
    bcm = pexpect.spawn('/root/start_bcm.170')
    bcm.expect('BCM.0>')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    autobcm_pb2_grpc.add_AutoBCMServicer_to_server(AutoBCM(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
