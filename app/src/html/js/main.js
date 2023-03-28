export default {
    name: 'App',
    data() {
        return {
            currentStatus: {
                'hood_status': null,
                'rear_rh_door_status': null,
                'rear_lh_door_status': null,
                'trunk_status': null
            },
            client: null,
            readyToGo: false,
        };
    },
    methods: {
        onConnect() {
            this.client.subscribe("sampleApp/currentHoodOpenStatus");
            this.client.subscribe("sampleApp/currentDoorStateRearRH");
            this.client.subscribe("sampleApp/currentDoorStateRearLH");
            this.client.subscribe("sampleApp/currentTrunkOpenStatus");
            this.getAllStatus();
        },

        getAllStatus() {
            var message = new Messaging.Message("");
            message.destinationName = "sampleapp/getAllStatus";
            this.client.send(message)
        },
        onConnectionLost(obj) {
            console.log("connection lost");
            console.log(obj)
        },
        initialize() {
            var r = (Math.round(Math.random() * 255)).toString(16);
            var g = (Math.round(Math.random() * 255)).toString(16);
            var b = (Math.round(Math.random() * 255)).toString(16);
            this.client = new Messaging.Client("broker.mqttdashboard.com", Number(8000), r + g + b);
            console.log("Connection attempeted with client id: " + r + g + b);
            this.client.onConnect = this.onConnect
            this.client.onConnectionLost = this.onConnectionLost
            this.client.onMessageArrived = this.onMessageArrived

            var options = {
                timeout: 3,
                onSuccess: this.onConnect
            };
            this.client.connect(options)
        },
        onMessageArrived(message) {
            var payload = JSON.parse(message.payloadString);
            this.currentStatus[payload.name] = payload.status;
            this.readyToGo = !(Object.values(this.currentStatus).includes(true
            ));
            console.log(this.currentStatus);

        }
    },
    mounted() {
        this.initialize();
    },
    template: `
    <div class="container">
        <h1 style="text-align: center;">Vehicle Status</h1>
        <div class="shadow p-3 mt-2 mb-5 bg-body rounded" style="width: 60%;margin-left: 20%;">
            <div class="row">
                <div class="d-flex justify-content-end" style="padding-right: 3rem;">
                    <button type="button" class="btn btn-primary btn-sm"  @click ="getAllStatus()">
                        Get Current Status
                    </button>
                </div>
            </div>
            <div class="column">
                <div class="col-md-6">
                    <div>
                        <div class="form-check form-switch d-flex flex-row">
                            <label style="font-weight: bold;">
                                    Vehicle Status:
                            </label>
                            <input class="form-check-input p-disabled " type="checkbox" id="flexSwitchCheckChecked1"
                                :disabled='true'
                                checked style="margin: 7px 10px; cursor:not-allowed; opacity: 100%;"
                                :style= "
                                    [readyToGo ? 
                                        {'background-color': 'green','border-color': 'green'} 
                                        : {'background-color': 'red','border-color': 'red'}]" 
                            />
                            <label v-if="readyToGo">
                                Ready to Go
                            </label>
                            <label v-else>
                                Not Ready
                            </label>
                        </div>
                        <div class="form-check form-switch">
                            <lable style="font-weight: bold;">
                                Vehicle Health:
                            </lable>
                        </div>
                        <div class="form-check form-switch cloumn" style="padding-left: 70px;">
                            <div class="d-flex flex-row">
                                <label class="form-label">
                                    Trunk Status:&nbsp
                                </label>
                                <label v-if="currentStatus.trunk_status" style="color: red;font-weight: bold;">
                                    Opened
                                </label>
                                <label v-else style="color: green;font-weight: bold;">
                                    Closed
                                </label>
                            </div>
                            <div class="d-flex flex-row">
                                <label class="form-label">
                                    Hood Status:&nbsp
                                </label>
                                <label v-if="currentStatus.hood_status" style="color: red;font-weight: bold;">
                                    Opened
                                </label>
                                <label v-else style="color: green;font-weight: bold;">
                                    Closed
                                </label>
                            </div>
                            <div class="d-flex flex-row">
                                <label class="form-label">
                                    Rear Right Door Status:&nbsp
                                </label>
                                <label v-if="currentStatus.rear_rh_door_status" style="color: red;font-weight: bold;">
                                    Opened
                                </label>
                                <label v-else style="color: green;font-weight: bold;">
                                    Closed
                                </label>
                            </div>
                            <div class="d-flex flex-row">
                                <label class="form-label">
                                    Rear Left Door Status:&nbsp
                                </label>
                                <label v-if="currentStatus.rear_lh_door_status" style="color: red;font-weight: bold;">
                                    Opened
                                </label>
                                <label v-else style="color: green;font-weight: bold;">
                                    Closed
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
};