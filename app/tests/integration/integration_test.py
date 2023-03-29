# Copyright (c) 2022 Robert Bosch GmbH and Microsoft Corporation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

import json
import pytest
from sdv.test.inttesthelper import IntTestHelper
from sdv.test.mqtt_util import MqttClient
import can
import time

# GET_SPEED_REQUEST_TOPIC = "sampleapp/getSpeed"
# GET_SPEED_RESPONSE_TOPIC = "sampleapp/getSpeed/response"

@pytest.mark.asyncio
async def test_can_bus():
    bus1 = can.interface.Bus('test', bustype='virtual')
    bus2 = can.interface.Bus('test', bustype='virtual')

    msg1 = can.Message(arbitration_id=0x3B2, data=[1])
    bus1.send(msg1)
    msg2 = bus2.recv()

    #assert msg1 == msg2
    assert msg1.arbitration_id != msg2.arbitration_id
    assert msg1.data == msg2.data
    assert msg1.timestamp != msg2.timestamp
    
@pytest.mark.asyncio
async def test_socket_can_bus():
    bustype = 'virtual'
    channel = 'vcan0' # can0 on non-virtual physical bus

    bus = can.interface.Bus(channel=channel, bustype=bustype, bitrate=500000)
    for i in range(6000):
        #driver door open, key in run, engine off
        msg = can.Message(
            is_extended_id=False, 
            arbitration_id=0x3B2, 
            data=[0x77, 0x80, 0x06, 0x80, 0xD9, 0x06, 0x00, 0x00])
        print(msg)
        bus.send(msg)
        time.sleep(0.01) # send every 10 ms
        


