<template>
<div class="content">
  <div class="container-fluid">
    <card>
      <font-awesome-icon :icon="['fas', 'network-wired']" size=lg color='rgb(0, 0, 0)' /> <strong> Networks</strong>
      <hr>
      <table width="100%">
        <tr>
          <th>Name</th>
          <th>Scope</th>
          <th>Driver</th>
          <th>Created</th>
        </tr>


        <tr v-for='(network,i) in networks' :key="network" id='networkInfoCard'>
          <router-link :to="{path: 'dockernetwork', query: {net_id: networks_id[i]}}">
            <td width='10%'>{{network}}</td>
          </router-link>
          <td width='25%'>{{scopes[i]}}</td>
          <td width='25%'>{{drivers[i]}}</td>
          <td width='25%'>{{createdTimes[i]}}</td>
        </tr>
      </table>
      <hr>
      <button type="button" class="btn btn-primary btn-sm" @click='showCreate = !showCreate'>
        <font-awesome-icon :icon="['fas', 'plus']" size=sm color='rgb(255, 255, 255)' />
        Create
      </button>

    </card>

    <card v-show='showCreate'>
      <div class="container-fluid">
        <table width='100%'>
          <tr width='10%'>
            <td>
              <font-awesome-icon :icon="['far', 'plus-square']" size=lg color='rgb(0, 0, 0)' /> <strong> New network</strong>
            </td>
          </tr>
        </table>
        <hr>

        <table width='100%'>
          <tr>
            <td width='33%'>
              <div class="input-group mb-3">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="inputGroup-sizing-default">Name</span>
                </div>
                <input v-model='create_name' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
              </div>
            </td>
            <td width='33%'>
              <div class="input-group mb-3">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="inputGroup-sizing-default">Driver</span>
                </div>
                <select v-model='create_driver' class="custom-select" id="inputGroupSelect01">
                  <option selected>Choose...</option>
                  <option>bridge</option>
                  <option>host</option>
                  <option>overlay</option>
                </select>
              </div>
            </td>
            <td width='33%'>
              <div class="input-group mb-3">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="inputGroup-sizing-default">Scope</span>
                </div>
                <select v-model='create_scope' class="custom-select" id="inputGroupSelect01">
                  <option selected>Choose...</option>
                  <option>local</option>
                  <option>global</option>
                  <option>swarm</option>
                </select>
              </div>
            </td>
          </tr>
        </table>
        <table width='100%'>
          <tr>
            <td width='48%'>
              <div class="input-group mb-3">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="inputGroup-sizing-default">Subnet</span>
                </div>
                <input placeholder="e.g. 10.10.123.0/24" v-model='create_subnet' ype="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
              </div>
            </td>
            <td></td>
            <td width='48%'>
              <div class="input-group mb-3">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="inputGroup-sizing-default">Gateway</span>
                </div>
                <input placeholder="e.g. 10.10.123.1" v-model='create_gateway' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
              </div>
            </td>
          </tr>


        </table>

        <table>
          <tr>
            <td width='15%'>
              <strong>IPv6 Enable: </strong>
              <toggle-button v-model="create_ipv6" :value='true' :labels="{checked: 'on', unchecked: 'off'}" />
            </td>

            <td width='82%'></td>
            <td>
              <button type="button" class="btn btn-secondary btn-sm" @click='showCreate = false'>
                Cancel
              </button>
            </td>

            <td>

              <button type="button" class="btn btn-primary btn-sm" @click='createNetwork(create_name, create_driver, create_scope, create_subnet, create_gateway, create_ipv6)'>
                Create
              </button>
            </td>
          </tr>
        </table>


  </div>
  </card>

</div>
</div>
</template>

<script>
import Card from '../../../components/Cards/Card.vue'
import {
  ToggleButton
} from 'vue-js-toggle-button'
// import { mapGetters, mapActions } from 'vuex'
// import LTable from '@/components/Table.vue'

export default {
  inject: ['reload'],

  name: 'DockerN',

  components: {
    Card,
    ToggleButton,
  },
  data() {
    return {
      networks: [],
      networks_id: [],

      scopes: [],
      drivers: [],
      createdTimes: [],

      create_name: '',
      create_driver: '',
      create_subnet: '',
      create_gateway: '',
      create_ipv6: false,
      create_scope: '',
      create_check_duplicate: '',

      showCreate: false,

    }
  },
  mounted() {
    this.axios.get('/api/docker/list_networks').then(response => {
      // console.log(response)
      var res_name = JSON.parse(response.data.result)['return_name'].slice(1, -1).split(',')
      var res_id = JSON.parse(response.data.result)['return_id'].slice(1, -1).split(',')
      var i;
      for (i = 0; i < res_name.length; i++) {
        this.networks.push(res_name[i].trim().slice(1, -1))
        var net_id = res_id[i].trim().slice(1, 13)
        this.networks_id.push(net_id)

        // console.log(res_id[i].trim().slice(1, 13))

        this.axios.get('/api/docker/inspect_network', {
          params: {
            network_id: net_id
          }
        }).then(response => {
          // console.log(JSON.parse(response.data.result)['return'])
          var res = JSON.parse(response.data.result)['return']
          this.scopes.push(res['Scope'])
          if (res['Driver'] == null) {
            this.drivers.push('-')
          } else {
            this.drivers.push(res['Driver'])
          }
          var time_1 = res['Created'].split('Z')[0].split('T')[0]
          var time_2 = res['Created'].split('Z')[0].split('T')[1].split('.')[0]
          this.createdTimes.push(time_1 + ' / ' + time_2)

        })

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

    createNetwork(create_name, create_driver, create_scope, create_subnet, create_gateway, create_ipv6){

        this.axios.get('/api/docker/create_network', {
            params: {
                create_name: create_name,
                create_driver: create_driver,
                create_scope: create_scope,
                create_subnet: create_subnet,
                create_gateway: create_gateway,
                create_ipv6: create_ipv6,
            }
        }).then(response => {
            // console.log(response)
            this.reload()
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
