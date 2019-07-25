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
                <button type="button"
                        class="btn btn-dark btn-lg"
                        v-b-modal="'bcmportwindow'"
                >
                  Select Ports
                </button>

              </td>
            </tr>
            <tr>
              <td>
                <div>
                  Selected items : {{ checkedPortNames }}
                </div>
                <br>
              </td>
            </tr>
            <tr>
              <td>
                <input
                  class="form-control"
                  v-model="form.vlanid"
                  id="VLAN ID"
                  placeholder="VLAN ID">
                <div class="text-danger">
                  <ul>
                    <li v-if="formErrors.badCharacters">VLAN ID must be a number.
                    </li>
                    <li v-if="formErrors.nameIsEmpty">You must specify a VLAN ID.
                    </li>
                  </ul>
                </div>

                <button type="button"
                        @click="sendRequest"
                        :ok-disabled="!isFormValid"
                        class="btn btn-dark btn-lg">
                  Do the thing
                </button>
                <br>

              </td>


            </tr>
          </table>
        </td>
        <td>
          <table width="500">
            <tr>
              <td>
                <button type="button"
                        @click="showPorts"
                        class="btn btn-dark btn-lg">
                  Update Port Status
                </button>
              </td>
            </tr>
            <tr>
              <td>
                {{portStatus}}
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
    <div>
      {{bottomText}}
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
                bottomText: "Hello",
                portStatus: "",
                isCheckAll: false,
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
                form: {
                    selectedPorts: "",
                    action: "Show VLANs",
                    vlanid: ""
                },
                formErrors: {
                    badCharacters: false,
                    fieldIsEmpty: true
                },
                actionsAvailable: ["Show VLANs", "Create VLAN", "Destroy VLAN", "Add ports to VLAN",
                    "Remove ports from VLAN", "Show port-based VLANs", "Set port-based VLANs"]
            }
        },
        mounted() {
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
            }
        },
        methods: {
            checkAll: function () {

                this.isCheckAll = !this.isCheckAll;
                this.ports = [];
                if (this.isCheckAll) { // Check all
                    for (var row = 0; row < this.portList.length; row++) {
                        for (var key in this.portList[row]) {
                            console.log(key);
                            this.ports.push(this.portList[row][key]);
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
            validateName() {
                console.log("called Validate")
                this.formErrors.badCharacters = this.form.vlanid.length > 0 && !this.form.vlanid.match(/^[0-9]*$/);
                this.formErrors.nameIsEmpty = this.form.vlanid.length === 0 && (this.form.action != "Show VLANs"
                    && this.form.action != "Show port-based VLANs");
            },
            generateURL() {
                var url = '';
                switch (this.form.action) {
                    case "Show VLANs":
                        url = '/api/bcm/show_vlans/';
                        break;
                    case "Create VLAN":
                        url = '/api/bcm/create_vlan/' + this.form.vlanid + '/';
                        if(this.form.selectedPorts.length > 0){
                            url +=this.form.selectedPorts;
                        }
                        break;
                    case "Destroy VLAN":
                        url = '/api/bcm/destroy_vlan/' + this.form.vlanid;
                        break;
                    case "Add ports to VLAN":
                        url = '/api/bcm/add_ports/' + this.form.vlanid + '/' + this.form.selectedPorts;
                        break;
                    case "Show port-based VLANs":
                        url = '/api/bcm/show_pvlans/';
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
            showPorts(){
                const url = '/api/bcm/show_active_ports/';
                axios.get(url).then((response)=>{
                    this.portStatus = response.data.result.result;
                })
            }
        },
        watch: {
            vlanid: function () {
                this.validateName()
            },
            selection: function () {
                this.validateName()
            },
            ports: function () {
                this.printValues()
            }
        }
    }
</script>
