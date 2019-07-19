<template>
<router-link to="./docker">
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
        <!-- {{inspect(test[0])}} -->
        <tr v-for="container in containers">
          <!-- <p>{{inspect('67588f30bc')}}</p> -->
          <td></td>
          <td>
            <router-link :to="'docker/dockercontainer/' + container">
              {{container}}
            </router-link>

          </td>
          <td>

          </td>

        </tr>



        <br>
      </table>


    </card>

  </div>
</router-link>
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
      var i;
      for (i = 1; i < containers.length; i++) {
        this.containers.push(containers[i].slice(2, -1).split(":")[1].trim())
      }

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
