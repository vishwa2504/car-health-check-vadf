import asyncio
import json
import logging
import signal

from sdv.util.log import (  # type: ignore
    get_opentelemetry_log_factory,
    get_opentelemetry_log_format,
)
from sdv.vdb.subscriptions import DataPointReply
from sdv.vehicle_app import VehicleApp, subscribe_topic
from vehicle import Vehicle, vehicle  # type: ignore

# Configure the VehicleApp logger with the necessary log config and level.
logging.setLogRecordFactory(get_opentelemetry_log_factory())
logging.basicConfig(format=get_opentelemetry_log_format())
logging.getLogger().setLevel("DEBUG")
logger = logging.getLogger(__name__)

HOOD_OPEN_STATUS_SUBSCRIPTION_TOPIC = "sampleApp/currentHoodOpenStatus"
DOOR_STATE_REAR_RH_SUBSCRIPTION_TOPIC = "sampleApp/currentDoorStateRearRH"
DOOR_STATE_REAR_LH_SUBSCRIPTION_TOPIC = "sampleApp/currentDoorStateRearLH"
TRUNK_OPEN_STATUS_SUBSCRIPTION_TOPIC = "sampleApp/currentTrunkOpenStatus"

GET_ALL_CURRENT_STATUS_TOPIC = "sampleapp/getAllStatus"

subscribeTopic = {
    'hood_status': "sampleApp/currentHoodOpenStatus",
    'rear_rh_door_status': "sampleApp/currentDoorStateRearRH",
    'rear_lh_door_status': "sampleApp/currentDoorStateRearLH",
    'trunk_status': "sampleApp/currentTrunkOpenStatus",
}


class SampleApp(VehicleApp):
    def __init__(self, vehicle_client: Vehicle):
        # SampleApp inherits from VehicleApp.
        super().__init__()
        self.Vehicle = vehicle_client

    async def mqttPublish(self, name: str, status):
        await self.publish_event(
            subscribeTopic[name],
            json.dumps({"name": name, "status": status}),
        )

    async def on_start(self):
        await self.Vehicle.Body.Hood.IsOpen.subscribe(self.on_hood_change)
        await self.Vehicle.Cabin.Door.Row2.Right.IsOpen.subscribe(
            self.on_rear_rh_door_change
        )
        await self.Vehicle.Cabin.Door.Row2.Left.IsOpen.subscribe(
            self.on_rear_lh_door_change
        )
        await self.Vehicle.Body.Trunk.Rear.IsOpen.subscribe(self.on_trunk_change)

    async def on_hood_change(self, data: DataPointReply):
        hood_status = data.get(self.Vehicle.Body.Hood.IsOpen).value
        await self.mqttPublish("hood_status", hood_status)

    async def on_trunk_change(self, data: DataPointReply):
        trunk_status = data.get(self.Vehicle.Body.Trunk.Rear.IsOpen).value
        await self.mqttPublish("trunk_status", trunk_status)

    async def on_rear_rh_door_change(self, data: DataPointReply):
        rear_rh_door_status = data.get(self.Vehicle.Cabin.Door.Row2.Right.IsOpen).value
        await self.mqttPublish("rear_rh_door_status", rear_rh_door_status)

    async def on_rear_lh_door_change(self, data: DataPointReply):
        rear_lh_door_status = data.get(self.Vehicle.Cabin.Door.Row2.Left.IsOpen).value
        await self.mqttPublish("rear_lh_door_status", rear_lh_door_status)

    @subscribe_topic(GET_ALL_CURRENT_STATUS_TOPIC)
    async def on_get_all_current_status_request_received(self, data: str) -> None:
        await self.mqttPublish(
            "hood_status", (await self.Vehicle.Body.Hood.IsOpen.get()).value
        )
        await self.mqttPublish(
            "trunk_status", (await self.Vehicle.Body.Trunk.Rear.IsOpen.get()).value
        )
        await self.mqttPublish(
            "rear_rh_door_status",
            (await self.Vehicle.Cabin.Door.Row2.Right.IsOpen.get()).value,
        )
        await self.mqttPublish(
            "rear_lh_door_status",
            (await self.Vehicle.Cabin.Door.Row2.Right.IsOpen.get()).value,
        )


async def main():
    """Main function"""
    logger.info("Starting SampleApp...")
    # Constructing SampleApp and running it.
    vehicle_app = SampleApp(vehicle)
    await vehicle_app.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
