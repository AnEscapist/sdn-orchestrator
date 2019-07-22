<template>
  <div>
    <div>
  <AgGridVue style="width: 500px; height: 150px;"
             class="ag-theme-balham"
             :columnDefs="columnDefs"
             :rowData="rowData"
             :gridOptions="gridOptions"
             @selection-changed="onSelectionChanged"
  >
  </AgGridVue>
    </div>
    <div>
  <h3>Selected: {{selected}}</h3>
    </div>
  </div>
</template>

<script>
  import {AgGridVue} from "ag-grid-vue"

  export default {
    name: "AgTableExample",
    components: {
      AgGridVue
    },
    data() {
      return {
        vmTableColumns: ['Name', 'State', 'Memory Usage', 'Memory Allocated', 'CPUs'], //todo: figure out how to implement running time
        columnDefs: [
          { headerName: 'Make', field: 'make', sortable: true, filter: true, checkboxSelection: true },
          { headerName: 'Model', field: 'model', sortable: true, filter: true },
          { headerName: 'Price', field: 'price', sortable: true, filter: true },
        ],
        rowData: [
          { make: 'Toyota', 'model': 'Celica', price: 35000 },
          { make: 'Ford', 'model': 'Mondeo', price: 32000 },
          { make: 'Porsche', 'model': 'Boxter', price: 72000 },
        ],
        gridOptions: {
          rowSelection: "multiple",
          rowMultiSelectWithClick: true,
          suppressCellSelection: true
        },
        selected: []
      }
    },
    mounted (){
      this.gridApi = this.gridOptions.api;
      this.gridColumnApi = this.gridOptions.columnApi;
  },
    methods: {
      onSelectionChanged(){
        let selection = this.gridApi.getSelectedRows();
        this.selected = selection
      }
    }
  }
</script>

<style scoped>

</style>
