<template>
  <div>
    <div class="content">
      <div class="mt-2">
        <AgGridVue style="width: 1220px; height: 300px;"
                   class="ag-theme-balham"
                   :columnDefs="columnDefs"
                   :rowData="rowData"
                   :gridOptions="gridOptions"
        >
        </AgGridVue>
      </div>
      <div class="text-center">
        <button type="button" class="btn btn-primary" @click="adjustValues">
          Submit
        </button>
      </div>
      <div>

      </div>
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
            rowData: [],
            data: [],
            columns: [...tableColumns],
            columnDefs: [
              { headerName: 'Slot', field: 'slot', sortable: true, checkboxSelection: true },
              { headerName: 'Device Name', field: 'device_name', sortable: true },
              { headerName: 'Interface', field: 'interface', sortable: true },
              { headerName: 'Current Driver', field: 'current_driver', sortable: false, editable: true },
              { headerName: 'Available Drivers', field: 'drivers', sortable: false},
              { headerName: 'Driver Type', field: 'driver_type', sortable: true }
            ],
            gridOptions: {
              suppressCellSelection: true
            },
          }
        },
        mounted() {
          this.gridApi = this.gridOptions.api;
          this.gridColumnApi = this.gridOptions.api;
          this.updateData()
        },
        methods: {
          updateData(){
            this.axios.get("/api/grpc/get_net_devices").then(response => {
              let res = JSON.parse(response.data.result.return)
              let tmp_list = [];
              this.data = res
              console.log(this.data)
              Object.values(res).forEach(function(i) {
                let tmp_dict = {
                  'slot': i.slot,
                  'device_name': i.device_name,
                  'interface': i.interface,
                  'current_driver': i.current_driver,
                  'drivers': i.drivers,
                  'driver_type': i.driver_type
                };
                tmp_list.push(tmp_dict)
              });
              this.rowData = tmp_list;
              console.log(this.rowData)
            });
          },
          adjustValues(){

            this.updateData();
          },
          bindDevice(node){
            this.axios.get('/api/grpc/dpdk_bind/', {
              params: {
                slot: node.data.slot,
                current_driver: node.current_driver
              }
            }).then(response => {
              console.log(JSON.parse(response.data.result.return));
              const sleep = (milliseconds) => {
                return new Promise(resolve => setTimeout(resolve, milliseconds))
              };
              sleep(1000).then(() => {})
            })
            // console.log("hello2")
          }
        }
    }
</script>

<style scoped>

</style>
