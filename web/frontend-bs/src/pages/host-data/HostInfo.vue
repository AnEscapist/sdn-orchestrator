<template>
  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-xl-3 col-md-6">
          <stats-card>
            <div slot="header" class="icon-warning">
              <i class="nc-icon nc-chart text-warning"></i>
            </div>
            <div slot="content">
              <p class="card-category">Capacity</p>
              <h4 class="card-title">{{ total_mem }}}</h4>
            </div>
            <div slot="footer">
              <i class="fa fa-refresh"></i>Updated now
            </div>
          </stats-card>
        </div>

        <div class="col-xl-3 col-md-6">
          <stats-card>
            <div slot="header" class="icon-success">
              <i class="nc-icon nc-light-3 text-success"></i>
            </div>
            <div slot="content">
              <p class="card-category">Revenue</p>
              <h4 class="card-title">$1,345</h4>
            </div>
            <div slot="footer">
              <i class="fa fa-calendar-o"></i>Last day
            </div>
          </stats-card>
        </div>

        <div class="col-xl-3 col-md-6">
          <stats-card>
            <div slot="header" class="icon-danger">
              <i class="nc-icon nc-vector text-danger"></i>
            </div>
            <div slot="content">
              <p class="card-category">Errors</p>
              <h4 class="card-title">23</h4>
            </div>
            <div slot="footer">
              <i class="fa fa-clock-o"></i>Last day
            </div>
          </stats-card>
        </div>

        <div class="col-xl-3 col-md-6">
          <stats-card>
            <div slot="header" class="icon-info">
              <i class="nc-icon nc-favourite-28 text-primary"></i>
            </div>
            <div slot="content">
              <p class="card-category">Followers</p>
              <h4 class="card-title">+45</h4>
            </div>
            <div slot="footer">
              <i class="fa fa-refresh"></i>Updated now
            </div>
          </stats-card>
        </div>

      </div>

    </div>
  </div>
</template>

<script>
    import ChartCard from "../../components/Cards/ChartCard";
    import StatsCard from "../../components/Cards/StatsCard";
    import LTable from "../../components/Table";

    export default {
        name: "HostInfo",
        components: [
          LTable,
          ChartCard,
          StatsCard
        ],
        data() {
          return {
            total_mem: this.getTotalMem
          };
        },
        methods: {
          getValues(func) {
            // const token = sessionStorage.getItem('token')
            const URL = `/api/grpc/${func}`
            this.$axios({
              method: 'get',
              url: URL,
              headers: {
                'Content-Type': 'application/json',
                // Authorization: `Bearer ${token}`
              }
            })
              .then(res => {
                const res_val = JSON.parse(res.data.result)['return']
                // this.data_values[`${func}`] = res_val
                return res_val
              })
              .catch(err => {
                console.log(err)
              })
          }
        },
        computed: {
          getTotalMem:() => this.getValues("total_mem")
        }
    }
</script>

<style scoped>

</style>
