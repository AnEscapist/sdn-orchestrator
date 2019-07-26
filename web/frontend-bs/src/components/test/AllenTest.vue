<template>

  <div>
    <table width="1000">
      <tr>
        <td>
          <table width="500">
            <tr>
              <td>
                <form>
                  <div class="form-row">
                    <label for="vlanAction">Action</label>
                    <select id="vlanAction"
                            v-model="form.action"
                            class="custom-select mr-sm-2">
                      <option v-for="action in actionsAvailable">{{action}}</option>
                    </select>
                  </div>
                </form>
                <br>
                Your selection: {{form.action}}
                <br>
                <br>
              </td>

            </tr>
            <tr>
              <td>


                <b-modal id="bcmportwindow" title="Select Ports" scrollable>
                  <div>
                    <!-- Check All -->
                    <input type='checkbox' @click='checkAll()' v-model='isCheckAll'> Check All

                    <!-- Checkboxes list -->
                    <table width="400">
                      <tr v-for='row in portList'>
                        <td v-for='port in row'>
                          <input type='checkbox' v-bind:value='port' v-model='ports' @change='updateCheckall()'>
                          <label :for="port"> {{port}}</label>
                        </td>
                      </tr>
                    </table>
                  </div>
                </b-modal>
                <div id="PBMButton">
                  <button type="button"
                          class="btn btn-dark btn-lg"
                          :disabled="!canSelectPBM"
                          v-b-modal="'bcmportwindow'"
                  >
                    Select Ports
                  </button>
                  <div>
                    Selected ports : {{ checkedPortNames }}
                  </div>
                  <div class="text-danger">
                    <ul>
                      <li v-if="formErrors.noPortsSelected">Please select ports.
                      </li>
                    </ul>
                  </div>
                </div>
                <br>
              </td>
            </tr>
            <tr>
              <td>


                <b-modal id="bcmportwindow2" title="Select Untagged Ports" scrollable>
                  <div>
                    <!-- Check All -->
                    <input type='checkbox' @click='checkAll2()' v-model='isCheckAll2'> Check All

                    <!-- Checkboxes list -->
                    <table width="400">
                      <tr v-for='row in portList'>
                        <td v-for='port in row'>
                          <input type='checkbox' v-bind:value='port' :disabled="!portIsSelected(port)" v-model='ports2'
                                 @change='updateCheckall2()'>
                          <label :for="port"> {{port}}</label>
                        </td>
                      </tr>
                    </table>
                  </div>

                </b-modal>
                <div id="UBMButton">
                  <button type="button"
                          class="btn btn-dark btn-lg"
                          v-b-modal="'bcmportwindow2'"
                          :disabled="!canSelectUBM"
                  >
                    Select Untagged Ports
                  </button>
                  <div>
                    Selected untagged ports : {{ checkedPortNames2 }}
                  </div>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <br>
              </td>
            </tr>
            <tr>
              <td>
                <div id="VLANTextField">
                  <label for="VLAN ID">VLAN ID</label>
                  <input
                    class="form-control"
                    v-model="form.vlanid"
                    :disabled="!canSelectVLANID"
                    id="VLAN ID"
                    placeholder="VLAN ID">
                  <div class="text-danger">
                    <ul>
                      <li v-if="formErrors.badCharacters">VLAN ID must be a number.
                      </li>
                      <li v-if="formErrors.fieldIsEmpty">You must specify a VLAN ID.
                      </li>
                    </ul>
                  </div>
                </div>


                <button type="button"
                        @click="sendRequest"
                        :disabled="!isFormValid"
                        class="btn btn-dark btn-lg">
                  Run
                </button>
                <br>
              </td>
            </tr>
          </table>
        </td>
        <td>
          <table width="20">
            <!--            Just an empty table for the sake of spacing-->
          </table>
        </td>
        <td>
          <table width="400">

            <label for="PortStatus">
              Port Status
            </label>
            <tr id="PortStatus">

              <td>
                <li v-for="line in portStatusList[0]">
                  {{line}}
                </li>
              </td>
              <td>
                <li v-for="line in portStatusList[1]">
                  {{line}}
                </li>
              </td>
            </tr>
            <tr>
              <td>
                <button type="button"
                        @click="showPorts"
                        class="btn btn-dark btn-lg">
                  Update Port Status
                </button>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
    <div>
      <label for="output">
        Output
      </label>
      <li id="output" v-for="line in bottomText.split(/[\n]/)">
        {{line}}
      </li>
    </div>
    <!--    <br>-->
    <!--    <h1>{{test}}</h1>-->
  </div>
</template>
<script>
    import axios from 'axios';
    import Table from "../index";

    export default {
        components: {Table},
        data() {
            return {
                checkedPortNames: "",
                checkedPortNames2: "",
                bottomText: "",
                portStatus: "",
                isCheckAll: false,
                isCheckAll2: false,
                portList: [["ge1", "ge2", "ge3", "ge4"],
                    ["ge5", "ge6", "ge7", "ge8"],
                    ["ge9", "ge10", "ge11", "ge12"],
                    ["ge13", "ge14", "ge15", "ge16"],
                    ["ge17", "ge18", "ge19", "ge20"],
                    ["ge21", "ge22", "ge23", "ge24"],
                    ["ge25", "ge26", "ge27", "ge28"],
                    ["ge29", "ge30", "ge31", "ge32"],
                    ["xe0", "xe1", "xe2", "xe3"],
                    ["xe4", "xe5", "xe6", "xe7"],
                    ["xe8", "xe9", "xe10", "xe11"]],
                ports: [],
                ports2: [],
                form: {
                    selectedPorts: "",
                    selectedPorts2: "",
                    action: "Show VLANs",
                    vlanid: ""
                },
                formErrors: {
                    badCharacters: false,
                    fieldIsEmpty: true,
                    noPortsSelected: false
                },
                actionsAvailable: ["Show VLANs", "Create VLAN", "Destroy VLAN", "Add ports to VLAN",
                    "Remove ports from VLAN", "Show port-based VLANs", "Set port-based VLANs"]
            }
        },
        mounted() {
            this.validateName();
            this.renderButtons();
            axios.get('/api/bcm/show_active_ports/').then((response) => {
                this.portStatus = response.data.result.result
            })
        },
        computed: {
            vlanid() {
                return this.form.vlanid
            },
            selection() {
                return this.form.action
            },
            isFormValid() {
                return Object.values(this.formErrors).every(error => !error)
            },
            canSelectUBM() {
                return this.form.action == "Add ports to VLAN" ||
                    this.form.action == "Create VLAN";
            },
            canSelectPBM() {
                const action = this.form.action;
                return action == "Add ports to VLAN" ||
                    action == "Remove ports from VLAN" ||
                    action == "Create VLAN" ||
                    action == "Set port-based VLANs";
            },
            canSelectVLANID() {
                const action = this.form.action;
                return action == "Add ports to VLAN" ||
                    action == "Remove ports from VLAN" ||
                    action == "Create VLAN" ||
                    action == "Set port-based VLANs" ||
                    action == "Destroy VLAN";
            },

            portStatusList() {
                const raw = this.portStatus.split(/[\n]/);
                const firsthalf = raw.slice(0, 22);
                console.log("This is the first half" + firsthalf);
                const secondhalf = raw.slice(22, 45);
                console.log("This is the second half" + secondhalf);
                return [firsthalf, secondhalf];
            }
        },
        methods: {
            checkAll: function () {

                this.isCheckAll = !this.isCheckAll;
                this.ports = [];
                if (this.isCheckAll) { // Check all
                    for (var row = 0; row < this.portList.length; row++) {
                        for (var key in this.portList[row]) {
                            this.ports.push(this.portList[row][key]);
                        }
                    }
                }
            },
            checkAll2: function () {

                this.isCheckAll2 = !this.isCheckAll2;
                this.ports2 = [];
                if (this.isCheckAll2) { // Check all
                    for (var row = 0; row < this.portList.length; row++) {
                        for (var key in this.portList[row]) {
                            this.ports2.push(this.portList[row][key]);
                        }
                    }
                }
            },
            updateCheckall: function () {
                const length = 48;
                if (this.ports.length == length) {
                    this.isCheckAll = true;
                } else {
                    this.isCheckAll = false;
                }
            },
            updateCheckall2: function () {
                const length = 48;
                if (this.ports2.length == length) {
                    this.isCheckAll = true;
                } else {
                    this.isCheckAll = false;
                }
            },
            printValues: function () {
                this.form.selectedPorts = "";
                this.checkedPortNames = "";
                var key;
                // Read Checked checkboxes value
                for (key = 0; key < this.ports.length - 1; key++) {
                    this.form.selectedPorts += this.ports[key] + ",";
                    this.checkedPortNames += this.ports[key] + ", ";
                }
                if (this.ports.length > 0) {
                    this.form.selectedPorts += this.ports[key];
                    this.checkedPortNames += this.ports[key];
                }
            },
            printValues2: function () {
                this.form.selectedPorts2 = "";
                this.checkedPortNames2 = "";
                var key;
                // Read Checked checkboxes value
                for (key = 0; key < this.ports2.length - 1; key++) {
                    this.form.selectedPorts2 += this.ports2[key] + ",";
                    this.checkedPortNames2 += this.ports2[key] + ", ";
                }
                if (this.ports2.length > 0) {
                    this.form.selectedPorts2 += this.ports2[key];
                    this.checkedPortNames2 += this.ports2[key];
                }
            },
            validateName() {
                console.log("called Validate")
                this.formErrors.badCharacters = this.form.vlanid.length > 0 && !this.form.vlanid.match(/^[0-9]*$/);
                this.formErrors.fieldIsEmpty = this.form.vlanid.length === 0 && (this.form.action != "Show VLANs"
                    && this.form.action != "Show port-based VLANs");
                console.log(this.isFormValid);
            },
            validatePorts(){
                this.formErrors.noPortsSelected = this.ports.length == 0 &&
                    (this.form.action == "Add ports to VLAN" ||
                  this.form.action == "Remove ports from VLAN" ||
                    this.form.action == "Set port-based VLANs");
            },
            portIsSelected(port) {
                return this.ports.includes(port);
            },
            generateURL() {
                var url = '';
                switch (this.form.action) {
                    case "Show VLANs":
                        url = '/api/bcm/show_vlans/';
                        break;
                    case "Create VLAN":
                        url = '/api/bcm/create_vlan/' + this.form.vlanid + '/';
                        if (this.form.selectedPorts.length > 0) {
                            url += this.form.selectedPorts;
                            if (this.form.selectedPorts2.length > 0) {
                                url += '/' + this.form.selectedPorts2;
                            }
                        }
                        break;
                    case "Destroy VLAN":
                        url = '/api/bcm/destroy_vlan/' + this.form.vlanid;
                        break;
                    case "Add ports to VLAN":
                        url = '/api/bcm/add_ports/' + this.form.vlanid + '/' + this.form.selectedPorts + '/';
                        if (this.form.selectedPorts2.length > 0) {
                            url += this.form.selectedPorts2;
                        }
                        break;
                    case "Remove ports from VLAN":
                        url = '/api/bcm/remove_ports/' + this.form.vlanid + '/' +
                            this.form.selectedPorts;
                        break;
                    case "Show port-based VLANs":
                        url = '/api/bcm/show_pvlans/';
                        break;
                    case "Set port-based VLANs":
                        url = '/api/bcm/set_pvlans/' + this.form.vlanid + '/' +
                            this.form.selectedPorts;
                        break;
                    default:
                        console.log("Failed to translate get request");
                }
                return url;
            },
            sendRequest() {
                var url = this.generateURL();
                console.log(url);
                axios.get(url).then((response) => {
                    this.bottomText = response.data.result.result
                })
                //     .then(() => {
                //     console.log(this.bottomText)
                // })
            },
            showPorts() {
                const url = '/api/bcm/show_active_ports/';
                axios.get(url).then((response) => {
                    this.portStatus = response.data.result.result;
                })
            },
            renderButtons() {
                var x = document.getElementById("PBMButton");
                if (!this.canSelectPBM) {
                    x.style.display = "none";
                } else {
                    x.style.display = "block";
                }
                x = document.getElementById("UBMButton");
                if (!this.canSelectUBM) {
                    x.style.display = "none";
                } else {
                    x.style.display = "block";
                }
                x = document.getElementById("VLANTextField");
                if (!this.canSelectVLANID) {
                    x.style.display = "none";
                } else {
                    x.style.display = "block";
                }
            }
        },
        watch: {
            vlanid: function () {
                this.validateName()
            },
            selection: function () {
                this.validateName();
                this.validatePorts();
                this.renderButtons()
            },
            ports: function () {
                this.printValues();
                this.validatePorts()
            },
            ports2: function () {
                this.printValues2()
            }
        }
    }
</script>
<style>
  #UBMButton {
    width: 400px;
  }

  #PBMButton {
    width: 400px;
  }

  #VLANTextField {
    width: 500px;
  }
</style>
