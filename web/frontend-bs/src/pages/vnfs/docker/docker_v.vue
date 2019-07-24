<template>
<div class="content">
  <div class="container-fluid">
    <card>
      <font-awesome-icon :icon="['fas', 'cubes']" size=lg color='rgb(0, 0, 0)' /> <strong> Volumes</strong>
      <hr>
      <table width="100%">
        <tr>
          <th>Name</th>
          <th>Drivers</th>
          <th>Created</th>
        </tr>


        <tr v-for='(vol,i) in volumes' id='volInfoCard'>
          <router-link :to="{path: 'dockervolume', query: {name: vol}}">
            <td width='10%'>{{vol}}</td>
          </router-link>
          <td>{{drivers[i]}}</td>
          <td>{{createdAt[i]}}</td>
        </tr>
      </table>
      <hr>
      <button type="button" class="btn btn-primary btn-sm" @click='showCreate = !showCreate'>
        <font-awesome-icon :icon="['fas', 'plus']" size=sm color='rgb(255, 255, 255)' />
        Create
      </button>
    </card>

    <card v-show="showCreate">

      <font-awesome-icon :icon="['far', 'plus-square']" size=lg color='rgb(0, 0, 0)' /> <strong> Create Volume</strong>

      <hr>
      <div class="pull-choice">
        <table>
          <tr>
            <td>
              <form class="form-inline">
                <strong style="font-size:15px">Name: &nbsp</strong>
                <input type="text" placeholder="e.g. myVolume" v-model="newName">
              </form>
            </td>

          </tr>
        </table>
        <br>
        <table>
          <tr>
            <td width='43%'></td>
            <td width='42%'></td>
            <td>
              <button type="button" class="btn btn-secondary btn-sm" @click='showCreate = false'>
                Cancel
              </button>
            </td>
            <td>
                <button type="button" class="btn btn-primary btn-sm" @click="createVol(newName)">
                  <font-awesome-icon :icon="['fas', 'plus']" size=sm /> <strong style="font-size:13px"> Create</strong>
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
// import { mapGetters, mapActions } from 'vuex'
// import LTable from '@/components/Table.vue'

export default {
  inject: ['reload'],
  name: 'DockerV',

  components: {
    Card,

  },
  data() {
    return {
      volumes: [],
      createdAt: [],
      inspect: '',
      drivers: [],
      newName: '',

      showCreate: false,
    }
  },
  mounted() {
    this.axios.get('/api/docker/list_volumes').then(response => {
      var res = JSON.parse(response.data.result)['return']
      var vols = res.slice(1, -1).split(',')
      var i;
      for (i = 0; i < vols.length; i++) {
        this.volumes.push(vols[i].trim().slice(1, -1))
      }

      this.createdAt = []
      this.drivers = []
      var j;
      for (j = 0; j < this.volumes.length; j++) {

        this.axios.get('/api/docker/inspect_volume', {
          params: {
            name: this.volumes[j]
          }
        }).then(response => {
          var inspect = JSON.parse(response.data.result)['return']
          this.inspect = inspect
          this.createdAt.push(inspect['CreatedAt'].slice(0, -1).split('T').join(' / '))
          this.drivers.push(inspect['Driver'])
        })
      }
      // console.log(this.volumes)


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

    createVol(newName){
        this.axios.get('/api/docker/create_volume', {
          params: {
            name: newName,
          }
        }).then(response => {
          // console.log(JSON.parse(response.data.result))
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

#volInfoCard {
  font-family: Arial, sans-serif;
  font-size: 15px;
  background-color: rgb(248, 248, 248);
  border-bottom: 2px solid white;
  height: 25px;
  padding-top: 3px;
  padding-bottom: 3px;

}

#volInfoCard:hover {
  background-color: rgb(233, 233, 233);
}

/*todo: consider making this global*/
</style>
