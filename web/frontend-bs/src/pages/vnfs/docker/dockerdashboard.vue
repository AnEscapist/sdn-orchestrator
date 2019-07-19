<template>
<div class="content">
  <div class="container-fluid">
    <card>
      <font-awesome-icon :icon="['fas', 'database']" size=lg color='rgb(0, 0, 0)' /> <strong> Containers</strong>
      <hr>

      <table>
        <th>Name</th>
        <th>Status</th>
        <!-- {{state}} -->
        <!-- {{inspect(containers[0].trim().slice(1, -1))}} -->
        <tr v-for='(container,i) in containers' :key="container">
          <td>{{container.trim().slice(1, -1)}}</td>

        </tr>
      </table>

      <!-- <LTable class="table-hover"
               :columns="containerCol"
               :data="Object.values(containerInfo)">
           </LTable> -->
    </card>
    <!--      todo: notifications fo VNF status changes-->
  </div>
</div>
</template>

<script>
import Card from '../../../components/Cards/Card.vue'
// import { mapGetters, mapActions } from 'vuex'
// import LTable from '@/components/Table.vue'

export default {
  name: 'DockerDashboard',

  components: {
    Card,

  },
  data() {
    return {
      containers: [],
      images: [],
      client: '',
      info: '',
      state: [],
    }
  },
  mounted() {
    this.axios.get("/api/docker/list_containers").then(response => {
      var res = JSON.parse(response.data.result)['return']
      var containers = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
      this.containers = containers
      // var i;
      // for (i = 1; i < containers.length; i++) {
      //   this.containers.push(containers[i].slice(2, -1).split(":")[1].trim())
      // }

    });
    this.axios.get("/api/docker/list_images").then(response => {
      var res = JSON.parse(response.data.result)['return']
      var images = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
      this.images = images
    });
    this.axios.get("/api/docker/client_info").then(response => {
      var res = JSON.parse(response.data.result)
      var client = JSON.parse(res['return'])
      this.client = client
    });
    // this.axios.get("/api/docker/inspect_container", {
    //   params: {
    //     id: 'c33833f1cd43',
    //   }
    // }).then(response => {
    //   var res = JSON.parse(response.data.result)['return']
    //   console.log(res['Image'])
    // });
  },
  methods: {
    notifyVue(verticalAlign, horizontalAlign) {
      const color = Math.floor((Math.random() * 4) + 1)
      this.$notifications.notify({
        message: `<span>Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer.</span>`,
        icon: 'nc-icon nc-app',
        horizontalAlign: horizontalAlign,
        verticalAlign: verticalAlign,
        type: this.type[color]
      })
    },
    get_status(containers) {

      var i;
      for (i = 0; i < containers.length; i++) {
        this.axios.get("/api/docker/inspect_container", {
          params: {
            id: containers[i].trim().slice(1, -1)
          }
        }).then(response => {
          var x = JSON.parse(response.data.result)['return']['State']['Status']
          console.log('x', x)
          this.state.push(x)
          console.log(this.state, '======')
          console.log(JSON.parse(response.data.result)['return']['State']['Status'])
        });
      }
    },


  }
}
</script>

<style scoped>
.info {
  font-size: 15px;
  padding-left: 10px;
  padding-top: 12px;
  padding-bottom: 12px;
  /*border: 1px solid rgb(180, 180, 180);*/
  /*background: rgb(240, 240, 240);*/
  text-align: left;
  ;
}

/*todo: consider making this global*/
</style>
