<template>

  <div>
    <table>
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
        </td>
        <td>
          <!-- Check All -->
          <input type='checkbox' @click='checkAll()' v-model='isCheckAll'> Check All

          <!-- Checkboxes list -->
          <ul>
            <li v-for='port in portList'>
              <input type='checkbox' v-bind:value='port' v-model='ports' @change='updateCheckall()'>{{ port }}
            </li>
          </ul>

          <!-- Print -->
          <input type='button' @click='printValues()' value='Select these Ports'>

          <br>
          Selected items : {{ form.selectedPorts }}

        </td>


      </tr>
    </table>

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
                checkedNames: [],
                test: "Hello",
                isCheckAll: false,
                portList: ["ge1", "ge2", "ge3", "ge4", "ge5", "ge6", "ge7", "ge8", "ge9", "ge10",
                    "ge11", "ge12", "ge13", "ge14", "ge15", "ge16", "ge17", "ge18", "ge19", "ge20",
                    "ge21", "ge22", "ge23", "ge24", "ge25", "ge26", "ge27", "ge28", "ge29", "ge30",
                    "ge31", "ge32", "ge33", "ge34", "ge35", "xe0", "xe1", "xe2", "xe3", "xe4",
                    "xe5", "xe6", "xe7", "xe8", "xe9", "xe10", "xe11", "xe12"],
                ports: [],
                form: {
                    selectedPorts: "",
                    action: "Show VLANs"
                },
                actionsAvailable: ["Show VLANs", "Create VLAN"]
            }
        },
        // mounted() {
        //     axios.get('/api/bcm/show_vlans').then((response) => {
        //         this.test = response.data.result.result
        //     }).then(() => {
        //         console.log(this.test)
        //     })
        // },
        methods: {
            checkAll: function () {

                this.isCheckAll = !this.isCheckAll;
                this.ports = [];
                if (this.isCheckAll) { // Check all
                    for (var key in this.portList) {
                        this.ports.push(this.portList[key]);
                    }
                }
            },
            updateCheckall: function () {
                if (this.ports.length == this.portList.length) {
                    this.isCheckAll = true;
                } else {
                    this.isCheckAll = false;
                }
            },
            printValues: function () {
                this.form.selectedPorts = "";
                var key;
                // Read Checked checkboxes value
                for (key = 0; key < this.ports.length - 1; key++) {
                    this.form.selectedPorts += this.ports[key] + ", ";
                }
                if (this.ports.length>0) {
                    this.form.selectedPorts += this.ports[key];
                }
            }
        }
    }
</script>
