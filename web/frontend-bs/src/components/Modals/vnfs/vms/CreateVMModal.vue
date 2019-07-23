<template>
  <div>
    <b-modal
      ok-title="Create VNF"
      @show="onShow"
      @ok="onCreateVNF"
      id="vm-create-modal">
      <h2>{{vmCreateForm.hugepageMemoryAvailable}} blah {{vmCreateForm.memoryAvailable}}</h2>
      <h2>{{vmVCPUOptions}}</h2>
      <form>
        <div class="form-row">
          <!--          <div class="form-group col-md-6">-->
          <!--            <label for="inputEmail4">Email</label>-->
          <!--            <input type="email" class="form-control" id="inputEmail4" placeholder="Email">-->
          <!--          </div>-->
          <!--          <div class="form-group col-md-6">-->
          <!--            <label for="inputPassword4">Password</label>-->
          <!--            <input type="password" class="form-control" id="inputPassword4" placeholder="Password">-->
          <!--          </div>-->
          <label for="vmName">VNF Name</label>
          <input
                 class="form-control"
                 v-model="form.vmName"
                 id="vmName"
                 placeholder="name">
        </div>
        <div class="form-row">
          <label for="vmImageName">Image</label>
          <select id="vmImageName"
                  v-model="form.vmImage"
                  class="custom-select mr-sm-2">
            <option selected>Vyatta Router</option>
            <option>...</option>
          </select>
        </div>
        <div class="form-row">
          <div class="form-group col-md-4">
            <label for="vmCPUCount">vCPUs</label>
            <select id="vmCPUCount"
                    v-model="form.vmCPUs"
                    class="custom-select mr-sm-2">
              <option selected>1</option>
              <option>...</option>
            </select>
          </div>
          <div v-if="!form.hugepagesEnabled"
               class="form-group col-md-4">
            <label for="vmMemory">Memory</label>
            <select id="vmMemory"
                    class="custom-select mr-sm-2">
              <option selected>4 GB</option>
              <option>...</option>
            </select>
          </div>
          <div v-if="form.hugepagesEnabled"
               class="form-group col-md-4">
            <label for="vmHugepageMemory">Hugepage Memory</label>
            <select id="vmHugepageMemory"
                    class="custom-select mr-sm-2">
              <option selected>4 GB</option>
              <option>...</option>
            </select>
          </div>
          <div class="form-group col-md-4">
            <div><label>Hugepage Memory</label></div>
            <ToggleButton v-model="form.hugepagesEnabled" :height=35 :width=130 :font-size=16 :labels="{checked: 'Enabled', unchecked: 'Disabled'}"></ToggleButton>
          </div>
        </div>
<!--        <div class="form-group">-->
<!--          <div><label>Hugepages</label></div>-->
<!--          <ToggleButton :height=35 :width=80></ToggleButton>-->
<!--        </div>-->
      </form>
    </b-modal>
  </div>
</template>

<script>
  import Switches from 'vue-switches';
  import { ToggleButton } from 'vue-js-toggle-button'
  import axios from 'axios';
  import {mapGetters, mapActions} from 'vuex'

  export default {
    name: "CreateVMModal",
    components: {
      Switches, ToggleButton
    },
    data() {
      return {
        form: {
          vmName: "",
          vmImage: "Vyatta Router",
          vmCPUs: 1,
          vmMemory: 4,
          hugepagesEnabled: false
        },
        show: true,
      }
    },
    computed: {
      ...mapGetters([
        'vmCreateForm', 'vmVCPUOptions', 'vmMemoryOptions', 'vmHugepageMemoryOptions'
      ])
    },
    methods: {
      ...mapActions([
        'createVM', 'updateVCPUsAvailable', 'updateMemoryAvailable', 'updateHugepageMemoryAvailable'
      ]),
      onCreateVNF(){
        this.createVM({...this.form}).then(this.clearForm());
      },
      clearForm(){
        this.form.vmName = "";
      },
      onShow(){
        this.updateVCPUsAvailable();
        this.updateMemoryAvailable();
        this.updateHugepageMemoryAvailable();
        this.clearForm();
      }
    }
  }
</script>

<style scoped>
  select:-moz-focusring {
    color: transparent;
    text-shadow: 0 0 0 #000;
  }

  .raised {
    vertical-align: 10px
  }
</style>
