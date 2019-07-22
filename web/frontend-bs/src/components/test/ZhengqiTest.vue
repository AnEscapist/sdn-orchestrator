<template>
<div>
  <card>
    <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />
    <strong> Docker on uCPE ({{client['Name']}}) </strong>
    <span class="badge badge-success">Running</span>
    <hr>

    <table width='100%'>
      <tr>
        <td width='45%'>
          <router-link to="./docker_c">
            <div class="container-fluid">

              <font-awesome-icon :icon="['fas', 'database']" size=lg color='rgb(68, 68, 68)' />
              <strong> {{client['Containers']}} containers - </strong>
              <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(81, 164, 81)' />
              {{client['ContainersRunning']}}
              <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(237, 187, 66)' />
              {{client['ContainersPaused']}}
              <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(204, 68, 74)' />
              {{client['ContainersStopped']}}
              <hr>
            </div>
          </router-link>
        </td>
        <td></td>
        <td width='45%'>
          <router-link to="./docker_i">
            <div class="container-fluid">
              <font-awesome-icon :icon="['fas', 'clone']" size=lg color='rgb(68, 68, 68)' /> <strong> {{client['Images']}} images</strong>
              <hr>
            </div>
          </router-link>
        </td>
      </tr>

      <tr>
        <td width='48%'>
          <router-link to="./docker_n">
            <div class="container-fluid">

              <font-awesome-icon :icon="['fas', 'network-wired']" size=lg color='rgb(68, 68, 68)' />
              <strong> {{networks}} Networks</strong>

              <hr>
            </div>
          </router-link>
        </td>
        <td></td>
        <td width='48%'>
          <router-link to="./docker_v">
            <div class="container-fluid">
              <font-awesome-icon :icon="['fas', 'boxes']" size=lg color='rgb(68, 68, 68)' />
              <strong> {{volumes}} Volumes</strong>
              <hr>
            </div>
          </router-link>
        </td>
      </tr>
    </table>
  </card>

</div>
</template>

<script>
export default {
  name: "ZhengqiTest",
  data: function() {
    return {
      containers: [],
      images: [],
      client: '',
      info: '',
      networks: 0,
      volumes: 0,
    }


  },
  mounted() {
    this.axios.get("/api/docker/list_containers").then(response => {
      var res = JSON.parse(response.data.result)['return']
      var containers = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
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
      // console.log(response.data.result)
      var res = JSON.parse(response.data.result)
      var client = JSON.parse(res['return'])
      this.client = client
      this.networks = client['Plugins']['Network'].length
      this.volumes = client['Plugins']['Volume'].length
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
    inspect(id) {
      this.axios.get("/api/docker/inspect_container", {
        params: {
          id: id
        }
      }).then(response => {
        this.info = JSON.parse(response.data.result)['return']['Image']
      });
      return this.info
    },

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
