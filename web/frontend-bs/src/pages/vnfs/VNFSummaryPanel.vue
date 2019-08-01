<template>
  <card>
    <font-awesome-icon :icon="['fas', 'cubes']" size=lg color='rgb(111, 111, 111)' />
    <strong> Virtual Machines on uCPE (potato3) </strong>
<!--    todo: use zhengqi's thing to get potato3-->
    <span class="badge badge-success">Running</span>
    <hr>

    <table width='100%'>
      <tr>
        <td width='45%'>
          <router-link to="vms">
            <div class="container-fluid">
              <font-awesome-icon :icon="['fas', 'database']" size=lg color='rgb(68, 68, 68)' />
              <strong> {{vmCounts.total}} virtual machines - </strong>
              <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(81, 164, 81)' />
              {{vmCounts.running}}
              <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(237, 187, 66)' />
              {{vmCounts.paused}}
              <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(204, 68, 74)' />
              {{vmCounts.shutdown}}
              <hr>
            </div>
          </router-link>
        </td>
        <td></td>
        <td width='45%'>
          <router-link to="images">
            <div class="container-fluid">
              <font-awesome-icon :icon="['fas', 'clone']" size=lg color='rgb(68, 68, 68)' /> <strong> {{vmNumberImagesAvailable}} images</strong>
              <hr>
            </div>
          </router-link>
        </td>
      </tr>
    </table>
  </card>
</template>

<script>
  import {mapGetters, mapActions} from 'vuex'
    export default {
        name: "VNFSummaryPanel",
        components:{
        },
        computed: {
          ...mapGetters(['vnfList', 'vnfCount', 'vmTotalCount', 'vmCounts', 'vmNumberImagesAvailable'])
        },
        created() {
          this.updateVMInfo();
          this.updateVMImageInfo();
        },
        methods: {
          ...mapActions(['updateVMInfo', 'updateVMImageInfo'])
        }
    }
</script>

<style scoped>
  a {
    font-size: 20px;
    font-weight: bold;
    color: rgb(68, 68, 68);
  }

  .container-fluid {
    /* background: red; */
    /* width: 90%; */
    /* margin-left: 10px; */
    /* margin-right: 10px; */
    padding-top: 15px;
    margin-bottom: 12px;
    border: 1px solid rgb(226, 226, 226);
    border-radius: 4px;
  }

  .container-fluid:hover{
    background: rgb(240, 240, 240);
  }

</style>
