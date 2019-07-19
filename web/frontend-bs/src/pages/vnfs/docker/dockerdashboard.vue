<template>
<div class="content">
  <div class="container-fluid">
    <card>
      <font-awesome-icon :icon="['fas', 'database']" size=lg color='rgb(0, 0, 0)' /> <strong> Containers</strong>
      <ul v-for='container in containers'>
          <li>{{container}}</li>
      </ul>
    </card>
    <!--      todo: notifications fo VNF status changes-->
  </div>
</div>
</template>

<script>
import Card from '../../../components/Cards/Card.vue'
import SampleCard from '.././SampleCard'
import VNFSummaryPanel from '.././VNFSummaryPanel'
import VNFInfoPanel from '.././VNFInfoPanel'
import ZhengqiTest from '../../../components/test/ZhengqiTest'
import RogerTest from '../../../components/test/RogerTest'

export default {
  name: 'DockerDashboard',

  components: {
    Card,
    SampleCard,
    VNFSummaryPanel,
    VNFInfoPanel,
    ZhengqiTest,
    RogerTest
  },
  data() {
    return {
      type: ['', 'info', 'success', 'warning', 'danger'],
      notifications: {
        topCenter: false
      },
      containers: [],
      images: [],
      client: '',
      info: '',
    }
  },
  mounted() {
    this.axios.get("/api/docker/list_containers").then(response => {
    console.log(response.data.result)
      var res = JSON.parse(response.data.result)['return']
      var containers = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
      this.containers = containers
      console.log(this.containers)
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
    }
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
