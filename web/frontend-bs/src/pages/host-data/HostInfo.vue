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
              <p class="card-category">Total Memory</p>
              <h4 class="card-title">{{ total_mem }} kB</h4>
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
      name: "HostData",
      components: {
        LTable,
        StatsCard,
        ChartCard
      },
      data() {
        return {
          total_mem: '',
          avail_mem: '',

        }
      },
      mounted() {
        this.getTotalMem();
        this.getAvailableMem();
      },
      methods: {
        getTotalMem() {
          this.axios.get("/api/grpc/total_mem").then(response => {
            // console.log(response.data.result['return']);
            var res = response.data.result['return'];
            this.total_mem = res
          });
        },
        getAvailableMem() {
          this.axios.get("/api/grpc/avail_mem").then(response => {
            var res = response.data.result['return'];
            this.avail_mem = res
          })
        }
      }
    }
</script>

<style scoped>

</style>
