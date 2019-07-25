<template>
  <div class="w-100">
    <div>
      <div class="btn-toolbar justify-content-between"
           role="toolbar"
           aria-label="Actions Toolbar"
      >
        <VMActionsButtonGroup/>
        <div class="block btn-group mt-2"
             role="group"
             aria-label="Create VNF">
          <button type="button"
                  v-b-modal="'vm-create-modal'"
                  class="btn btn-secondary btn-sm"
                  >
            <font-awesome-icon :icon="['fas', 'plus-circle']"
                               size=sm
                               color='rgb(255, 255, 255)'/>
            New VNF
          </button>
          <CreateVMModal></CreateVMModal>
        </div>
      </div>
      <div>
        <input type="text"
               id="vm-table-filter-text-box"
               placeholder="Search..."
               v-model="filterText"
               class="form-control mt-2"
        />
      </div>
      <AgGridVue style="width: 1200px;"
                 class="ag-theme-balham mt-2"
                 id="vmTable"
                 :columnDefs="vmTableColumns"
                 :rowData="Object.values(vmInfo)"
                 :gridOptions="gridOptions"
                 quickFilterText=""
                 @selection-changed="onSelectionChanged"
      >
      </AgGridVue>
    </div>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import { AgGridVue } from "ag-grid-vue"
  import VMActionsButtonGroup from '../../Buttons/vnfs/vms/VMActionsButtonGroup'
  import CreateVMModal from '../../Modals/vnfs/vms/CreateVMModal'
  import VMConsoleRenderer from './VMConsoleRenderer'

  const AGENT_NAME = 'agent'; //todo: this is bad

  export default {
    name: "VMTableNew",
    components: { AgGridVue, VMActionsButtonGroup, CreateVMModal, VMConsoleRenderer },
    data() {
      return {
        vmTableColumns: [
          {
            headerName: 'Name',
            field: 'name',
            sortable: true,
            checkboxSelection: params => params.data.name !== AGENT_NAME
          }, //todo: find better way to do this
          { headerName: 'State', field: 'state', sortable: true },
          {headerName: 'Console', cellRendererFramework: VMConsoleRenderer},
          { headerName: 'Memory Usage', field: 'memory usage', sortable: true },
          { headerName: 'Memory Allocated', field: 'memory allocated', sortable: true },
          { headerName: 'CPUs', field: 'cpus', sortable: true },
        ],
        gridOptions: {
          rowSelection: "multiple",
          rowHeight: 34,
          domLayout: "autoHeight",
          rowMultiSelectWithClick: true,
          suppressCellSelection: true,
          suppressHorizontalScroll: true,
        },
        filterText: ''
      }
    },
    computed: {
      ...mapGetters([
        'vnfList', 'vnfCount', 'vmList', 'vmInfo', 'vmSelection', 'vmFilterText', 'vmStateFromName', 'vmAtLeastOneSelected', "vmAtLeastOneSelected", 'vmWebServerIPV4'
      ]),
    },
    mounted() {
      this.gridApi = this.gridOptions.api;
      this.gridColumnApi = this.gridOptions.columnApi;
      this.updateVMWebServerIPV4()
    },
    methods: {
      ...mapActions([
        'updateVMSelection', 'updateVMFilterText', 'startSelectedVMs', 'pauseSelectedVMs', 'killSelectedVMs', 'deleteSelectedVMs', 'updateVMWebServerIPV4'
      ]),
      onSelectionChanged() {
        let selection = this.gridApi.getSelectedRows();
        this.updateVMSelection(selection.map(row => row.name)); //todo: figure out why this warning happens
      },
      onGridReady(params){
        params.api.sizeColumnsToFit()
      },
      debug(){
        console.log("debug")
      }
    },
    watch: {
      filterText: function () {
        this.gridApi.setQuickFilter(this.filterText)
      }
    }
  }

</script>

<style scoped>
  .centered-table {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .btn-secondary {
    background-color: #4a148c;
  }

  .btn:focus, .btn:active {
    outline: none !important;
    box-shadow: none !important;
  }
</style>
