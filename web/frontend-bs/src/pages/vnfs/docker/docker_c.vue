<template>
<div class="content">
  <div class="container-fluid">
    <card>
      <font-awesome-icon :icon="['fas', 'database']" size=lg color='rgb(0, 0, 0)' /> <strong> Containers</strong>
      <hr>

      <table width="100%">
        <tr>
          <th>Name</th>
          <th>Images</th>
          <th>Status</th>
        </tr>


        <tr v-for='(container,i) in containers' :key="container" id='containerInfoCard'>
          <router-link :to="{path: 'dockercontainer', params: {name: container}, query: {name: container}}">
            <td width='10%'>{{container}}</td>
          </router-link>
          <td>{{images[i]}}</td>
          <td v-if="status[i] == 'running' ">
            <h6><span class="badge badge-pill badge-success">{{status[i]}}</span></h6>
          </td>
          <td v-else-if="status[i] == 'exited' ">
            <h6><span class="badge badge-pill badge-danger">{{status[i]}}</span></h6>
          </td>
          <td v-else>
            <h6><span class="badge badge-pill badge-primary">{{status[i]}}</span></h6>
          </td>
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
  name: 'DockerC',

  components: {
    Card,

  },
  data() {
    return {
      containers: [],
      images: [],
      client: '',
      info: '',
      status: [],
      all_img: [],
      name_tag: '',
    }
  },
  mounted() {
    this.axios.get("/api/docker/list_containers").then(response => {
      var res = JSON.parse(response.data.result)['return']
      var containers = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
      // this.containers = containers
      var i;
      for (i = 0; i < containers.length; i++) {
        // console.log(containers[i].trim().slice(1, -1))
        this.containers.push(containers[i].trim().slice(1, -1))
      }

    });

    this.axios.get('/api/docker/containers_status').then(response => {
      // console.log(JSON.parse(response.data.result)['return'])
      var res = JSON.parse(response.data.result)['return']
      var regex = /\[(.+?)\]/g;
      // console.log(res.match(regex2));
      var status = res.match(regex);
      var i;
      for (i = 0; i < status.length; i++) {
        this.status.push(status[i].substring(status[i].indexOf('[') + 1, status[i].indexOf(']')))
      }
    });

    this.axios.get("/api/docker/list_images").then(response => {
      var res = JSON.parse(response.data.result)['return']
      var regex = /\<(.+?)\>/g;
      var imgs = res.match(regex)
      var i;
      for (i = 0; i < imgs.length; i++) {
        this.all_img.push(imgs[i].substring(imgs[i].indexOf(':') + 3, imgs[i].indexOf('>') - 1))
      }
    });

    this.axios.get('api/docker/containers_images').then(response => {
      var res = JSON.parse(response.data.result)['return']
      var regex = /\<(.+?)\>/g;
      var images = res.match(regex)
      var i;
      for (i = 0; i < images.length; i++) {
        this.images.push(images[i].substring(images[i].indexOf(':') + 3, images[i].indexOf('>') - 1))
      }
    })

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
    pullImg(name_tag){
        if (name_tag.includes(':')){
            var name = name_tag.split(':')[0]
            var tag = name_tag.split(':')[1]
        } else {
            var name = name_tag
            var tag = 'latest'
        }
        this.axios.get('/api/docker/pull_image', {
            params: {
                name: name,
                tag: tag,
                timeout: 1000
            }
        }).then(response => {
            console.log(JSON.parse(response.data.result))
        })

    }
    // get_status(containers) {
    //
    //   var i;
    //   for (i = 0; i < containers.length; i++) {
    //     this.axios.get("/api/docker/inspect_container", {
    //       params: {
    //         id: containers[i].trim().slice(1, -1)
    //       }
    //     }).then(response => {
    //       var x = JSON.parse(response.data.result)['return']['State']['Status']
    //       console.log('x', x)
    //       this.state.push(x)
    //       console.log(this.state, '======')
    //       console.log(JSON.parse(response.data.result)['return']['State']['Status'])
    //     });
    //   }
    // },


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


#containerInfoCard {
  font-family: Arial, sans-serif;
  font-size: 15px;
  background-color: rgb(248, 248, 248);
  border-bottom: 2px solid white;
  height: 25px;
  padding-top: 3px;
  padding-bottom: 3px;

}

#containerInfoCard:hover {
  background-color: rgb(233, 233, 233);
}

/*todo: consider making this global*/
</style>
