<template>
  <div class="content">
    <div class="mt-2">
      <AgGridVue style="width: 1000px; height: 300px;"
                 class="ag-theme-balham"
                 :columnDefs="columnDefs"
                 :rowData="data"
                 :gridOptions="gridOptions"
      >
      </AgGridVue>
    </div>
  </div>
</template>
<script>
    import {AgGridVue} from "ag-grid-vue";

    const tableColumns = ['Slot', 'Device Name', 'Interface', 'Driver', 'Driver Type']
    export default {
        name: "HostInfoNetworkDevices",
        components: {
          AgGridVue
        },
        data () {
          return {
            columns: [...tableColumns],
            columnDefs: [
              { headerName: 'Slot', field: 'slot', sortable: true, checkboxSelection: true },
              { headerName: 'Device Name', field: 'device_name', sortable: true },
              { headerName: 'Interface', field: 'interface', sortable: true },
              { headerName: 'Driver', field: 'driver',
                sortable: true,
                editable: true,
                cellEditor: "agSelectCellEditor",
                cellEditorParams: {
                  values: []
                }
              },
              { headerName: 'Driver Type', field: 'driver_type', sortable: true }
            ],
            data: [],
            gridOptions: {
              suppressCellSelection: true
            },
          }
        },
        mounted() {
          this.gridApi = this.gridOptions.api;
          this.gridColumnApi = this.gridOptions.api;
          this.getDevices()
        },
        methods: {
          getDevices(){
            this.axios.get("/api/grpc/get_net_devices").then(response => {
              var res = JSON.parse(response.data.result.return)
              var tmp_list = []
              // console.log(res)
              Object.values(res).forEach(function(i) {
                var tmp_dict = {
                  'slot': i.slot,
                  'device_name': i.device_name,
                  'interface': i.interface,
                  'driver': i.drivers,
                  'driver_type': i.driver_type
                };
                tmp_list.push(tmp_dict)
              });
              this.data = tmp_list;
              console.log(this.data)
            });
          }
        }
    }
</script>

<style scoped>

</style>
