<template>
<div class="content">
  <div class="container-fluid">
    <card>
      <font-awesome-icon :icon="['fas', 'cubes']" size=lg color='rgb(0, 0, 0)' /> <strong> Volumes</strong>
      <hr>
      <table width="100%">
        <tr>
          <th>Name</th>
          <th>Created</th>
        </tr>


        <tr v-for='(vol,i) in volumes' id='volInfoCard'>
          <router-link :to="{path: 'dockerimage', params: {name: vol}, query: {name: vol}}">
            <td width='10%'>{{vol}}</td>
          </router-link>
          <td width='25%'>{----</td>
          <!-- <td width='25%'>{{createTimes[i]}}</td>
          <td width='10%'>
            &nbsp&nbsp
            <font-awesome-icon v-show="busy[i] == 'yes'" :icon="['fas', 'check-circle']" size=sm color='#00bd56' />
            <font-awesome-icon v-show="busy[i] == 'no'" :icon="['fas', 'times-circle']" size=sm color='rgb(251, 0, 0)' />
          </td> -->
        </tr>
      </table>

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
      createdTimes: [],
      inspect: ''
    }
  },
  mounted() {
    this.axios.get('/api/docker/list_volumes').then(response => {
      var res = JSON.parse(response.data.result)['return']
      var regex = /\<(.+?)\>/g;
      var vols = res.match(regex)
      var i;
      for (i = 0; i < vols.length; i++) {
        this.volumes.push(vols[i].substring(vols[i].indexOf(':') + 2, vols[i].indexOf('>')))
      }

      var j;
      for (j = 0; j < this.volumes.length; j++) {
        this.createTimes = []
        this.axios.get('/api/docker/inspect_volume', {
          params: {
            name: this.volumes[j]
          }
        }).then(response => {
          console.log(response.data.result)
          var inspect = JSON.parse(response.data.result)['return']
          this.inspect = inspect
          // console.log(inspect)
          // this.sizes.push((parseFloat(inspect['Size']) / 1000000).toFixed(1))
          // this.createTimes.push(inspect['Created'].split('.')[0].split('T').join(' / '))
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
