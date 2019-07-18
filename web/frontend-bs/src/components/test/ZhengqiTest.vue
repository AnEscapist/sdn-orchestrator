<template>
<div>
  <card>
    <!-- <h1>Zhengqi's Playground</h1> -->
    <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />
    <strong> Docker on uCPE ({{client['Name']}}) </strong>
    <span class="badge badge-success">Running</span>
    <hr>
    <table>
      <tr>
        <td width='30px'></td>
        <td width='100px'>
          <font-awesome-icon :icon="['fas', 'info-circle']" size=lg color='rgb(111, 111, 111)' />
          <strong> Info: </strong>
        </td>
        <router-link to="dockercontainers">
          <td width='250px'>
            <font-awesome-icon :icon="['fas', 'database']" size=sm color='rgb(111, 111, 111)' />
            {{client['Containers']}} containers -
            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(81, 164, 81)' />
            {{client['ContainersRunning']}}
            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(237, 187, 66)' />
            {{client['ContainersPaused']}}
            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(204, 68, 74)' />
            {{client['ContainersStopped']}}
          </td>
        </router-link>



        <td width='120px'>
          <font-awesome-icon :icon="['fas', 'clone']" size=sm color='rgb(111, 111, 111)' />
          {{client['Images']}} images
        </td>
        <td>
          <font-awesome-icon :icon="['fas', 'microchip']" size=sm color='rgb(111, 111, 111)' />
          {{client['NCPU']}} CPU
        </td>
      </tr>
      <br>
    </table>

    <table cellspacing='20'>
      <tr>
        <th width='30px'></th>
        <th>Contaiers</th>
        <th>Images</th>
        <th>Status</th>
        <th>Ports</th>
      </tr>
      <tr v-for='container in containers'>
        <!-- <p>{{inspect('67588f30bc')}}</p> -->
        <td></td>
        <td>
            {{container.slice(1,-1).split(":")[1]}}
        </td>
        <td>
            <!-- {{inspect('c33833f1cd')}} -->
            {{container.slice(1,-1).split(":")[1].trim()}}
            <!-- {{typeof(container.slice(1,-1).split(":")[1].trim())}} -->
            <!-- {{inspect(container.slice(1,-1).split(":")[1].trim())}} -->
        </td>

      </tr>



      <br>
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
    }


  },
  mounted() {
    this.axios.get("/api/docker/list_containers").then(response => {
      var res = JSON.parse(response.data.result)['return']
      var containers = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
      this.containers = containers
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

</style>
