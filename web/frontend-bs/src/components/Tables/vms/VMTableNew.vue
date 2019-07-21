<template>
  <div>
    <div class="btn-group"
         role="group"
         aria-label="Actions">
      <button type="button"
              @click="startSelectedVMs"
              class="btn btn-success">Start
      </button>
    </div>
    <div class="mt-2">
      <AgGridVue style="width: 1000px; height: 300px;"
                 class="ag-theme-balham"
                 :columnDefs="vmTableColumns"
                 :rowData="Object.values(vmInfo)"
                 :gridOptions="gridOptions"
                 @selection-changed="onSelectionChanged"
      >
      </AgGridVue>
    </div>
    <!--    <h3>Selected: {{ vmSelection}}</h3>-->
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import { AgGridVue } from "ag-grid-vue"

  export default {
    name: "VMTableNew",
    components: { AgGridVue },
    data() {
      return {
        vmTableColumns: [
          { headerName: 'Name', field: 'name', sortable: true, checkboxSelection: true },
          { headerName: 'State', field: 'state', sortable: true },
          { headerName: 'Memory Usage', field: 'memory usage', sortable: true },
          { headerName: 'Memory Allocated', field: 'memory allocated', sortable: true },
          { headerName: 'CPUs', field: 'cpus', sortable: true },
        ],
        gridOptions: {
          rowSelection: "multiple",
          rowMultiSelectWithClick: true,
          suppressCellSelection: true
        },
      }
    },
    computed: {
      ...mapGetters([
        'vnfList', 'vnfCount', 'vmList', 'vmInfo', 'vmSelection'
      ])
    },
    mounted() {
      this.gridApi = this.gridOptions.api;
      this.gridColumnApi = this.gridOptions.columnApi;
    },
    methods: {
      ...mapActions([
        'updateVMSelection', 'startSelectedVMs'
      ]),
      onSelectionChanged() {
        let selection = this.gridApi.getSelectedRows();
        this.updateVMSelection(selection.map(row => row.name)); //todo: figure out why this error happens
      },
    }
  }
</script>

<style scoped>
  /*.ag-cell-focus, .ag-cell-no-focus{*/
  /*  border:none;*/
  /*}*/
  /*.no-border.ag-cell:focus{*/
  /*  border:none ;*/
  /*  outline:none;*/
  /*}*/
</style>
