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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import logging

import grpc

import autobcm_pb2
import autobcm_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('135.91.120.200:50051') as channel:
        stub = autobcm_pb2_grpc.AutoBCMStub(channel)

        #gotta split each request into its respective fields.
        #Do I want to take user input or should we just have
        #the user program all commands by hand?
        response = stub.CreateVLAN(autobcm_pb2.ConfigRequest(vlanid=100))
        print(response.message)
        response = stub.ShowVLANs(autobcm_pb2.ConfigRequest())
        print(response.message)
        #response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        #print("Greeter client received: " + response.message)

if __name__ == '__main__':
    logging.basicConfig()
    run()
