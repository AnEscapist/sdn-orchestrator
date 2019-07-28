<template>
<div class="content">
  <div class="container-fluid">
    <card>
        <font-awesome-icon :icon="['fas', 'network-wired']" size=lg color='rgb(0, 0, 0)' /> <strong> Networks</strong>
        <hr>
        <table width="100%">
          <tr>
            <th>Name</th>
            <th>Images</th>
            <th>Status</th>
          </tr>


          <tr v-for='(network,i) in networks' :key="network" id='networkInfoCard'>
            <router-link :to="{path: 'dockernetwork', query: {net_name: network}}">
              <td width='10%'>{{network}}</td>
            </router-link>
            <td width='33%'>===----===</td>
            <td>======</td>
          </tr>
        </table>
        <hr>
        <button type="button" class="btn btn-primary btn-sm" @click='showCreate = !showCreate'>
          <font-awesome-icon :icon="['fas', 'plus']" size=sm color='rgb(255, 255, 255)' />
          Create
        </button>

    </card>

  </div>
</div>
</template>

<script>
import Card from '../../../components/Cards/Card.vue'
// import { mapGetters, mapActions } from 'vuex'
// import LTable from '@/components/Table.vue'

export default {
  inject: ['reload'],

  name: 'DockerN',

  components: {
    Card,

  },
  data() {
    return {
        networks: [],
        networks_id: [],

    }
  },
  mounted() {
      this.axios.get('/api/docker/list_networks').then(response => {
          console.log(response)
          var res = JSON.parse(response.data.result)['return_name'].slice(1, -1).split(',')

          var i;
          for(i=0; i<res.length; i++){
              this.networks.push(res[i].trim().slice(1, -1))
          }
      })

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

a {
  color: rgb(38, 138, 255);
  font-family: Arial, sans-serif;
  font-weight: bold;
  font-size: 13px;
}

input {
  border: 2px solid rgb(200, 200, 200);
  border-radius: 4px;
  padding-left: 8px;
}

p {
  font-size: 12px;
  font-weight: bold;
}



#networkInfoCard {
  font-family: Arial, sans-serif;
  font-size: 15px;
  background-color: rgb(248, 248, 248);
  border-bottom: 2px solid white;
  height: 25px;
  padding-top: 3px;
  padding-bottom: 3px;

}

#networkInfoCard:hover {
  background-color: rgb(233, 233, 233);
}

/*todo: consider making this global*/
</style>
