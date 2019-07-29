<!--Todo
      -CONSTANTS
    NOTES:
      -Filesizes MUST be inputted in GB (there's some bad hardcoding that you can get rid of)
-->
<template>
  <div>
    <b-modal
      ok-title="Create VNF"
      @show="onShow"
      @ok="onCreateVNF"
      :ok-disabled="!isFormValid"
      id="vm-create-modal">
      <form>
        <!--        <h2>{{typeof(JSON.parse(vmBridgesAvailable))}}</h2>-->
        <!--        <h1>validity: {{isFormValid}}</h1>-->
        <!--        <h2>name: {{!!form.vmName.match(/^[a-zA-Z][-_a-zA-Z0-9]*$/)}} </h2>-->
        <!--&lt;!&ndash;        <h2>exist: {{vmList.contains(form.vmName)}}</h2>&ndash;&gt;-->
        <!--        <h2>exist: {{vmList.includes(form.vmName)}}</h2>-->
        <!--        <h2>vmList: {{vmList}}</h2>-->
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
            :maxlength="charLimit+1"
            id="vmName"
            placeholder="name">
          <div class="text-danger">
            <ul>
              <li v-if="formErrors.badStartingCharacter">VNF name must start with a letter</li>
              <li v-if="formErrors.badCharacters">VNF name can only contain alphanumeric characters, underscores, and
                dashes.
              </li>
              <li v-if="formErrors.nameExceedsCharLimit">VNF name can be at most {{charLimit}} characters long.</li>
              <li v-if="formErrors.vmExists && !formErrors.agent">VNF with name "{{form.vmName}}" already exists</li>
              <li v-if="formErrors.agent">VNF name "agent" is reserved</li>
            </ul>
          </div>
        </div>
        <div class="form-row">
          <label for="vmImageName">Image</label>
          <select id="vmImageName"
                  v-model="form.vmImage"
                  class="custom-select mr-sm-2">
            <option v-for="image in vmImagesAvailable">{{image}}</option>
          </select>
        </div>
        <div class="form-row">
          <div class="form-group col-md-4">
            <label for="vmCPUCount">vCPUs</label>
            <select id="vmCPUCount"
                    v-model="form.vmCPUs"
                    class="custom-select mr-sm-2">
              <option v-for="option in vmVCPUOptions">{{option}}</option>
            </select>
          </div>
          <div v-if="!form.hugepagesEnabled"
               class="form-group col-md-4">
            <label for="vmMemory">Memory</label>
            <select
              :disabled="isOutOfMemory"
              id="vmMemory"
              v-model="form.vmMemory"
              class="custom-select mr-sm-2">
              <option v-for="option in vmMemoryOptions">{{option}} GB</option>
              <option v-if="isOutOfMemory">0 GB</option>
            </select>
            <b-tooltip target="vmMemory"></b-tooltip>
          </div>
          <div v-if="form.hugepagesEnabled"
               class="form-group col-md-4">
            <label for="vmHugepageMemory">Hugepage Memory</label>
            <select :disabled=isOutOfHugepageMemory
                    id="vmHugepageMemory"
                    v-model="form.vmHugepageMemory"
                    class="custom-select mr-sm-2">
              <option v-for="option in vmHugepageMemoryOptions">{{option}} GB</option>
              <option v-if="isOutOfHugepageMemory">0 GB</option>
            </select>
          </div>
          <div class="form-group col-md-4">
            <div><label>Hugepage Memory</label></div>
            <ToggleButton v-model="form.hugepagesEnabled"
                          :height=35
                          :width=130
                          :font-size=16
                          :labels="{checked: 'Enabled', unchecked: 'Disabled'}"
                          @change="onHugepageToggle"
            />
          </div>
        </div>
        <!--        <div class="form-group">-->
        <!--          <div><label>Hugepages</label></div>-->
        <!--          <ToggleButton :height=35 :width=80></ToggleButton>-->
        <!--        </div>-->
        <div v-if="!form.hugepagesEnabled && isOutOfMemory"
             class="alert alert-danger">
          <span><strong>Out of Memory -</strong>  Cannot allocate sufficient memory.</span>
        </div>
        <div v-if="form.hugepagesEnabled && isOutOfHugepageMemory"
             class="alert alert-danger">
          <span><strong>Out of Memory -</strong>  Cannot allocate sufficient hugepage memory.</span>
        </div>
        <div class="form-row">
          <div
            class="form-group col-md-4">
            <label for="vmBridges">Bridge</label>
            <!--          todo: error handling on no bridge-->
            <select
              id="vmBridges"
              v-model="form.vmBridge"
              class="custom-select mr-sm-2">
              <option>No Bridge</option>
              <option v-for="bridge in vmBridgesAvailable">{{bridge}}</option>
            </select>
          </div>
          <div
            class="form-group col-md-4">
            <label for="vmOVSInterfaces">OVS Interfaces</label>
            <!--          todo: error handling on no bridge-->
            <div id="vmOVSInterfacesWrapper">
              <select
                id="vmOVSInterfaces"
                v-model="form.vmOVSInterfaceCount"
                :disabled="!form.hugepagesEnabled"
                class="custom-select mr-sm-2">
                <option v-for="i in vmOVSInterfaceOptions">{{i}}</option>
              </select>
              <b-tooltip target="vmOVSInterfacesWrapper"
                         title="You must enable hugepage memory to add OVS Interfaces."
                         :disabled="form.hugepagesEnabled"></b-tooltip>
            </div>
          </div>
        </div>
      </form>
    </b-modal>
  </div>
</template>

<script>
  import Switches from 'vue-switches';
  import { ToggleButton } from 'vue-js-toggle-button';
  import axios from 'axios';
  import { mapGetters, mapActions } from 'vuex';

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
          vmMemory: '4 GB',
          vmHugepageMemory: '4 GB',
          hugepagesEnabled: false,
          vmBridge: 'No Bridge',
          vmOVSInterfaceCount: 0
        },
        show: true,
        formErrors: {
          badStartingCharacter: false,
          badCharacters: false,
          vmExists: false,
          agent: false,
          nameExceedsCharLimit: false,
          nameIsEmpty: true,
          memoryError: false
        },
        charLimit: 15, //todo: make this a constant
      }
    },
    computed: {
      ...mapGetters([
        'vmCreateForm', 'vmVCPUOptions', 'vmMemoryOptions', 'vmHugepageMemoryOptions', 'vmImagesAvailable', 'vmList', 'vmBridgesAvailable', 'vmOVSInterfaceOptions'
      ]),
      vmName() {
        return this.form.vmName
      },
      isFormValid() {
        return Object.values(this.formErrors).every(error => !error)
      },
      initialFormMemory() {
        //todo: CLEAN THIS UP
        if (this.vmMemoryOptions.length === 0) {
          return '0 GB'; //todo: put this in a constant
        }
        return Math.max(Math.min(parseInt(this.form.vmMemory.split(" ")[0]), this.vmMemoryOptions.length), 1) + " GB" //max because after oom, vmMemory gets set to 0, s owithout the max it woudl be stuck at 0 from the min
      },
      initialFormHugepageMemory() {
        if (this.vmHugepageMemoryOptions.length === 0) {
          return '0 GB';
        }
        return Math.max(Math.min(parseInt(this.form.vmHugepageMemory.split(" ")[0]), this.vmHugepageMemoryOptions.length), 1) + " GB"
      },
      isOutOfMemory() {
        return this.form.vmMemory === '0 GB'
      },
      isOutOfHugepageMemory() {
        return this.form.vmHugepageMemory === '0 GB'
      }
    },
    methods: {
      ...mapActions([
        'createVM', 'updateVMVCPUsAvailable', 'updateVMMemoryAvailable', 'updateVMHugepageMemoryAvailable', 'updateVMImagesAvailable', 'updateVMBridgesAvailable'
      ]),
      onCreateVNF() {
        new Promise((resolve, reject) => {
          this.$emit('vm-create-load');
          this.$nextTick(resolve);
        }).then(() => {
          this.createVM({ ...this.form }).then(() => this.$emit('vm-create-finished'));
        }).then(() => {
          this.clearForm()
        });
      },
      clearForm() {
        this.form.vmName = "";
      },
      onShow() {
        this.updateVMVCPUsAvailable();
        this.updateVMMemoryAvailable().then(() => {
          this.form.vmMemory = this.initialFormMemory
        });
        this.updateVMHugepageMemoryAvailable().then(() => {
          this.form.vmHugepageMemory = this.initialFormHugepageMemory
        });
        this.updateVMImagesAvailable();
        this.updateVMBridgesAvailable();
        this.checkForMemoryError();
      },
      onHugepageToggle() {
        this.checkForMemoryError();
      },
      checkForMemoryError() {
        this.formErrors.memoryError = (!this.hugepagesEnabled && this.isOutOfMemory) || (this.hugepagesEnabled && this.isOutOfHugepageMemory)
      },
      validateName() {
        this.formErrors.badStartingCharacter = this.form.vmName.length > 0 && !this.form.vmName.match(/^[a-zA-Z]/);
        this.formErrors.agent = this.form.vmName === 'agent'; //todo: make constant
        this.formErrors.vmExists = this.vmList.includes(this.form.vmName);
        this.formErrors.badCharacters = this.form.vmName.length > 0 && !this.form.vmName.match(/^[-_a-zA-Z0-9]*$/);
        this.formErrors.nameExceedsCharLimit = this.form.vmName.length > this.charLimit;
        this.formErrors.nameIsEmpty = this.form.vmName.length === 0;
      }
    },
    watch: {
      vmName: function () {
        this.validateName()
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
