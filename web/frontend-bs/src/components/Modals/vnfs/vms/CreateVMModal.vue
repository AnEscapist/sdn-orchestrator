<!--Todo
      -CONSTANTS
    NOTES:
      -Filesizes MUST be inputted in GB (there's some bad hardcoding that you can get rid of)
-->
<template>
  <div>
    <b-modal
      ok-title="Create VM"
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
          <label for="vmName">VM Name</label>
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
                @change="onOVSInterfaceSelectChange"
                class="custom-select mr-sm-2">
                <option v-for="i in vmOVSInterfaceOptions">{{i}}</option>
              </select>
              <b-tooltip target="vmOVSInterfacesWrapper"
                         title="You must enable hugepage memory to add OVS Interfaces."
                         :disabled="form.hugepagesEnabled"></b-tooltip>
            </div>
          </div>
        </div>
        <div v-if="form.vmOVSInterfaceCount > 0">
          <div class="form-row">
            <!--          <label for="VLANConfiguration">VLAN Configuration</label>-->
            <b-card-header header-tag="header"
                           class="p-1 col-md-12"
                           role="tab">
              <b-button block
                        href="#"
                        v-b-toggle.accordion-1
                        variant="primary">OVS VLAN Configuration
              </b-button>
            </b-card-header>
          </div>
          <b-collapse id="accordion-1"
                      accordion="my-accordion"
                      role="tabpanel"
                      class="col-md-16">
            <!--                <b-card-text>I start opened because <code>visible</code> is <code>true</code></b-card-text>-->
            <!--                <b-card-text>more text</b-card-text>-->
            <!--              <div class="form-group row">-->
            <!--                <div class="col-md-6">-->
            <!--                <label class="col-sm-2 col-form-label">Interface 1</label>-->
            <!--&lt;!&ndash;                  <input type="text" class="form-control-plaintext"/>&ndash;&gt;-->
            <!--                  <input-->
            <!--                    class="form-control"-->
            <!--                    placeholder="name"/>-->
            <!--                </div>-->
            <!--              </div>-->
            <div v-for="(ovsInterface, index) in form.vmOVSInterfaceVLANs"
                 :key="index">
              <b-form inline>
                <label class='mr-sm-2'
                >VLAN Tag: eth{{index}}</label>
                <b-input
                  id="inline-form-input-name"
                  class="col-md-3"
                  :placeholder="MIN_VLAN_TAG + '-' + MAX_VLAN_TAG"
                  maxlength="4"
                  v-model="ovsInterface.vlan"
                ></b-input>
                <div class="text-danger">
                  <ul>
                    <li v-if="vmOVSInterfaceVLANInvalidTag[index]">Tag must be an integer in the range
                      {{MIN_VLAN_TAG}}-{{MAX_VLAN_TAG}}
                    </li>
                  </ul>
                </div>
              </b-form>
            </div>
          </b-collapse>
        </div>
      </form>
    </b-modal>
  </div>
</template>

<script>
  import Vue from 'vue'
  import Switches from 'vue-switches';
  import { ToggleButton } from 'vue-js-toggle-button';
  import { mapGetters, mapActions } from 'vuex';
  import { getZeroToNArray, getOneToNArray } from "@/utils/vmUtils";
  import vmOVSVLANInput from "@/components/Forms/vnfs/vms/vmOVSVLANInput"


  export default {
    name: "CreateVMModal",
    components: {
      Switches, ToggleButton, vmOVSVLANInput
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
          vmOVSInterfaceCount: 0,
          vmOVSInterfaceVLANs: [] //#todo: it's a bit flimsy to depend on the indices of an array
        },
        show: true,
        formErrors: {
          badStartingCharacter: false,
          badCharacters: false,
          vmExists: false,
          agent: false,
          nameExceedsCharLimit: false,
          nameIsEmpty: true,
          memoryError: false,
          vlanError: false,
        },
        vmOVSInterfaceVLANInvalidTag: [], //todo: extract vlan config into its own component and do events instead of v-model
        charLimit: 15, //todo: make this a constant
        MIN_VLAN_TAG: 1,
        MAX_VLAN_TAG: 4094,
        vmOVSInterfaceVLANsCache: [],
        vmOVSInterfaceCountCache: 0
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
      },
      ovsInterfaces() {
        return getZeroToNArray(this.form.vmOVSInterfaceCount - 1)
      },
      test() {
        return getOneToNArray(1)
      },
      vmOVSInterfaceCount() {
        return this.form.vmOVSInterfaceCount
      },
      vmOVSInterfaceVLANsExtracted() {
        return this.form.vmOVSInterfaceVLANs.map(x => x.vlan)
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
        this.form.vmOVSInterfaceVLANs.map((x, index) => {
          x.vlan = '';
        })
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
        console.log("toggle called");
        if(this.form.hugepagesEnabled){
          console.log("hugepages enabled");
          console.log(this.vmOVSInterfaceCountCache);
          console.log(this.vmOVSInterfaceVLANsCache);
          new Promise((resolve) => {resolve(this.form.vmOVSInterfaceCount = this.vmOVSInterfaceCountCache);
          }).then(() => {
            console.log('330', this.form.vmOVSInterfaceVLANs);
          for (let i = 0; i < this.vmOVSInterfaceCountCache; i++){
            // Vue.set(this.form.vmOVSInterfaceVLANs, i, {'vlan': this.vmOVSInterfaceVLANsCache[i]});
            this.form.vmOVSInterfaceVLANs[i].vlan = this.vmOVSInterfaceVLANsCache[i]
          }}
        ).then(() => console.log(this.form.vmOVSInterfaceVLANs))
        }
        else{
          this.form.vmOVSInterfaceCount = 0;
        }
      },
      onOVSInterfaceSelectChange() {
        // this.vmOVSInterfaceVLANs = this.ovsInterfaces.map(x => {return {vlan: ''}})
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
      },
      validateVLANs() {
        this.formErrors.vlanError = this.vmOVSInterfaceVLANInvalidTag.some(x => x)
      }
    },
    watch: {
      vmName: function () {
        this.validateName()
      },
      vmOVSInterfaceVLANsExtracted: {
        handler(newValue) {
          newValue.map((x, index) => {
            let valid = x !== '' && (isNaN(x) || parseInt(x) != x || !(this.MIN_VLAN_TAG <= parseInt(x) && parseInt(x) <= this.MAX_VLAN_TAG));
            Vue.set(this.vmOVSInterfaceVLANInvalidTag, index, valid);
            Vue.set(this.vmOVSInterfaceVLANsCache, index, x);
          })
        },
        deep: true
      },
      vmOVSInterfaceVLANInvalidTag: {
        handler(newValue) {
          this.validateVLANs();
        },
        deep: true
      }
      ,
      vmOVSInterfaceCount(newVal, oldVal) {
        if (this.form.hugepagesEnabled){
          this.vmOVSInterfaceCountCache = this.form.vmOVSInterfaceCount
        }
        if (newVal > oldVal) {
          for (let i = 0; i < newVal - oldVal; i++) {
            this.form.vmOVSInterfaceVLANs.push({ vlan: '' });
            if (i > this.vmOVSInterfaceVLANsCache.length){
              this.vmOVSInterfaceVLANsCache.push({vlan: '59'})
            }
            this.vmOVSInterfaceVLANInvalidTag.push(false)
          }
        }
        if (oldVal > newVal) {
          for (let i = 0; i < oldVal - newVal; i++) {
            this.form.vmOVSInterfaceVLANs.pop();
            this.vmOVSInterfaceVLANInvalidTag.pop()
          }
        }
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

  .btn:focus, .btn:active, .btn:active:focus, .btn.active:focus, .btn.focus, .btn:active.focus, .btn.active.focus {
    color: #ffffff;
    outline: none !important;
    box-shadow: none !important;
  }

  .btn-primary:hover,
  .open {
    color: #ffffff;
    border: 0;
    outline: none;
  }

</style>
