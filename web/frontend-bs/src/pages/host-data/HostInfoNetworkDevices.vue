<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">

        <div class="col-12">
          <card class="striped-tabled-with-hover"
                body-classes="table-full-width table-responsive">
            <template slot="header">
              <h4 class="card-title">Striped Table with Hover</h4>
              <p class="card-category">Here is a subtitle for this table</p>
            </template>
            <l-table class="table-hover table-striped"
                     :columns="table1.columns" :data="table1.data">
            </l-table>
          </card>
        </div>

        <div class="col-12">
          <card class="card-plain">
            <template slot="header">
              <h4 class="card-title">Table on Plain Background</h4>
              <p class="card-category">Here is a subtitle for this table</p>
            </template>
            <div class="table-responsive">
              <l-table class="table-hover"
                       :columns="table2.columns" :data="table2.data">
              </l-table>
            </div>
          </card>
        </div>

        <div class="col-12">
          <card class="strpied-tabled-with-hover"
                body-classes="table-full-width table-responsive">
            <template slot="header">
              <h4 class="card-title">Small table</h4>
              <p class="card-category">Here is a subtitle for this table</p>
            </template>
            <l-table class="table-hover table-striped table-sm"
                     :columns="table1.columns" :data="table1.data">
            </l-table>
          </card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
    import LTable from "../../components/Table.vue"
    import Card from "../../components/Cards/Card.vue"

    const tableColumns = ['slot', 'device_name', 'interface', 'driver', 'unused', 'driver_type']
    export default {
        name: "HostInfoNetworkDevices",
        components: {
          LTable,
          Card
        },
        data () {
          return {
            data2: [],
            table1: {
              columns: [...tableColumns],
              data: []
            },
            table2: {
              columns: [...tableColumns],
              data: []
            }
          }
        },
        mounted() {
          this.getDevices()
        },
        methods: {
          getDevices(){
            this.axios.get("/api/grpc/get_net_devices").then(response => {
              console.log(response.data.result.return)
              this.data2 = response.data.result.return;
              this.table1.data = this.data2
            });
          }
        }
    }
</script>

<style scoped>

</style>
