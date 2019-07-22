<template>
  <div class="centered-table mt-2">
    <div>
      <div class="block btn-group mt-2"
           role="group"
           aria-label="Actions">
        <button type="button"
                class="btn btn-success btn-sm"
                @click="startSelectedVMs">
          <font-awesome-icon :icon="['fas', 'play']"
                             size=sm
                             color='rgb(255,255,255)'/>
          Start
        </button>
        <!--      <button type="button" class="btn btn-danger btn-sm" @click="changeStatus('exited')">-->
        <!--        <font-awesome-icon :icon="['fas', 'square']" size=sm color='rgb(255, 255, 255)' />-->
        <!--        Stop-->
        <!--      </button>-->
        <button type="button"
                class="btn btn-primary btn-sm"
                @click="pauseSelectedVMs">
          <font-awesome-icon :icon="['fas', 'pause']"
                             size=sm
                             color='rgb(255, 255, 255)'/>
          Pause
        </button>
        <button type="button"
                class="btn btn-danger btn-sm"
                @click="killSelectedVMs">
          <font-awesome-icon :icon="['fas', 'skull-crossbones']"
                             size=sm
                             color='rgb(255, 255, 255)'/>
          Kill
        </button>
        <!--      <button type="button" class="btn btn-primary btn-sm" @click="changeStatus('restart')">-->
        <!--        <font-awesome-icon :icon="['fas', 'sync-alt']" size=sm color='rgb(255, 255, 255)' />-->
        <!--        Restart-->
        <!--      </button>-->
        <button type="button"
                class="btn btn-dark btn-sm"
                @click="deleteSelectedVMs">
          <font-awesome-icon :icon="['fas', 'trash-alt']"
                             size=sm
                             color='rgb(255, 255, 255)'/>
          Remove
        </button>
      </div>
      <div>
        <input type="text"
               id="vm-table-filter-text-box"
               placeholder="Search..."
               v-model="filterText"
               class="form-control mt-2"
        />
      </div>
      <AgGridVue style="width:1000px;"
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
<!--        <h3>Agent State: {{vmStateFromName('agent')}}</h3>-->
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import { AgGridVue } from "ag-grid-vue"

  const AGENT_NAME = 'agent'; //todo: this is bad

  export default {
    name: "VMTableNew",
    components: { AgGridVue },
    data() {
      return {
        vmTableColumns: [
          { headerName: 'Name', field: 'name', sortable: true, checkboxSelection: params => params.data.name !== AGENT_NAME }, //todo: find better way to do this
          { headerName: 'State', field: 'state', sortable: true },
          { headerName: 'Memory Usage', field: 'memory usage', sortable: true },
          { headerName: 'Memory Allocated', field: 'memory allocated', sortable: true },
          { headerName: 'CPUs', field: 'cpus', sortable: true },
        ],
        gridOptions: {
          rowSelection: "multiple",
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
        'vnfList', 'vnfCount', 'vmList', 'vmInfo', 'vmSelection', 'vmFilterText', 'vmStateFromName'
      ]),
    },
    mounted() {
      this.gridApi = this.gridOptions.api;
      this.gridColumnApi = this.gridOptions.columnApi;
    },
    methods: {
      ...mapActions([
        'updateVMSelection', 'updateVMFilterText', 'startSelectedVMs', 'pauseSelectedVMs', 'killSelectedVMs', 'deleteSelectedVMs'
      ]),
      onSelectionChanged() {
        let selection = this.gridApi.getSelectedRows();
        this.updateVMSelection(selection.map(row => row.name)); //todo: figure out why this warning happens
      },
    },
    watch: {
      filterText: function(){
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
</style>
