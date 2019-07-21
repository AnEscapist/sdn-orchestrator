<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">

        <div class="col-12">
          <card class="strpied-tabled-with-hover"
                body-classes="table-full-width table-responsive">
            <template slot="header">
              <h4 class="card-title">Network Devices</h4>
              <p class="card-category">List of NICs and details</p>
            </template>
            <l-table class="table-hover table-striped table-sm"
                     :columns="columns" :data="data">
            </l-table>
          </card>
        </div>
      </div>
    </div>
  </div>
  <div>
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
    import LTable from "../../components/Table.vue"
    import Card from "../../components/Cards/Card.vue"
    import {AgGridVue} from "ag-grid-vue";

    const tableColumns = ['Slot', 'Device Name', 'Interface', 'Driver', 'Unused', 'Driver Type']
    export default {
        name: "HostInfoNetworkDevices",
        components: {
          LTable,
          Card,
          AgGridVue
        },
        data () {
          return {
            columns: [...tableColumns],
            columnDefs: [
              { headerName: 'Slot', field: 'slot', sortable: true, checkboxSelection: true },
              { headerName: 'Device Name', field: 'device_name', sortable: true },
              { headerName: 'Interface', field: 'interface', sortable: true },
              { headerName: 'Driver', field: 'driver', sortable: true },
              { headerName: 'Unused', field: 'unused', sortable: true },
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
              this.data = Object.values(res)
            });
          }
        }
    }
</script>

<style scoped>

</style>
