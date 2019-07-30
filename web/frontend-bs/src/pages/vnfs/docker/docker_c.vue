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
          <router-link :to="{path: 'dockercontainer', query: {short_id: containers_id[i]}}">
            <td width='10%'>{{container}}</td>
          </router-link>
          <td width='33%'>{{images[i]}}</td>
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
              <font-awesome-icon :icon="['far', 'plus-square']" size=lg color='rgb(0, 0, 0)' /> <strong> New container</strong>
            </td>

            <td align='right' width='80%'>
              <router-link to="docker_i">
                <font-awesome-icon :icon="['fas', 'cloud-download-alt']" size=lg color='#1b7fbd' />
                <strong> Pull an image</strong>
              </router-link>
            </td>
          </tr>
        </table>
        <hr>
      </div>

      <div class="container-fluid">
        <table width='100%'>
          <tr>
            <td width='48%'>
              <div class="input-group mb-3">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="inputGroup-sizing-default">Name</span>
                </div>
                <input v-model='create_name' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
              </div>
            </td>
            <td></td>
            <td width='48%'>
              <div class="input-group mb-3">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="inputGroup-sizing-default">Image</span>
                </div>
                <select v-model='create_image' class="custom-select" id="inputGroupSelect01">
                  <option selected>Choose...</option>
                  <option v-for='img in all_img'>{{img}}</option>
                  <!-- <option value="2">Two</option>
                    <option value="3">Three</option> -->
                </select>
              </div>
            </td>
          </tr>
        </table>
        <table width='100%'>
          <tr>
            <td width='80%'>
              <div class="input-group mb-3">
                <div class="input-group-prepend">
                  <span class="input-group-text" id="inputGroup-sizing-default">Ports</span>
                </div>
                <input v-model='create_port' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
              </div>
            </td>
            <td width='0%'></td>
            <td stype='background:red' height='10px' style='padding-bottom: 15px' title="Valid format: container:host. e.g.: '2222/tcp:3333', '2222/tcp:None', '1111/tcp:(127.0.0.1, 111)' or '1111/tcp:[1234, 4567]'">

              <font-awesome-icon :icon="['fas', 'question-circle']" size=lg color='#1b7fbd' />
            </td>
          </tr>
        </table width='100%'>

        <card>
          <font-awesome-icon :icon="['fas', 'cog']" size=lg color='rgb(0, 0, 0)' />
          <strong> OVS configuration</strong>
          <hr>

          <table width='100%'>
            <tr>
              <!-- <td width='33%'>
                <div class="input-group mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text" id="inputGroup-sizing-default">OVS Interface</span>
                  </div>
                  <input v-model='ovs_int' type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
                </div>
              </td> -->
              <td width='20%'>
                <div class="input-group mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text" id="inputGroup-sizing-default">Interfaces</span>
                  </div>
                  <input v-model='int_port' placeholder="e.g.: 7, 8" type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
                </div>
              </td>
              <td width='33%'>
                <div class="input-group mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text" id="inputGroup-sizing-default">Interfaces ip</span>
                  </div>
                  <input v-model='int_ip' placeholder="e.g.: 10.10.81.123/24, 10.10.81.155/24" type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
                </div>
              </td>
              <td width='33%'>
                <div class="input-group mb-3">
                  <div class="input-group-prepend">
                    <span class="input-group-text" id="inputGroup-sizing-default">VLAN tag</span>
                  </div>
                  <input v-model='vlan_tag' placeholder="e.g.: 100, 101" type="text" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default">
                </div>
              </td>

            </tr>
          </table>

        </card>

        <table>
          <tr>
            <td width='50%'></td>
            <td width='40%'></td>
            <td>
              <button type="button" class="btn btn-secondary btn-sm" @click='showCreate = false'>
                Cancel
              </button>
            </td>
            <td>

              <button type="button" class="btn btn-primary btn-sm" @click='create_container(create_name, create_image, create_port, int_port, int_ip, vlan_tag)'>
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
// import { mapGetters, mapActions } from 'vuex'
// import LTable from '@/components/Table.vue'

export default {
  inject: ['reload'],

  name: 'DockerC',

  components: {
    Card,

  },
  data() {
    return {
      containers: [],
      containers_id: [],
      images: [],
      client: '',
      info: '',
      status: [],
      all_img: [],
      name_tag: '',
      showCreate: true,

      create_name: '',
      create_image: '',
      create_port: '',

      // ovs_int: '',
      int_port: '',
      int_ip: '',
      vlan_tag: '',


    }
  },
  mounted() {
    this.showCreate = false
    this.axios.get("/api/docker/list_containers").then(response => {
      var res = JSON.parse(response.data.result)['return']
      // console.log(res)
      var containers = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
      // this.containers = containers
      var i;
      for (i = 0; i < containers.length; i++) {
        // console.log(containers[i].trim().slice(1, -1))
        this.containers.push(containers[i].trim().slice(1, -1))
      }

    });

    this.axios.get('/api/docker/containers_id').then(response => {
      // console.log(JSON.parse(response.data.result)['return'])
      var res = JSON.parse(response.data.result)["return"]
      var containers_id = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
      var i;
      for (i = 0; i < containers_id.length; i++) {
        // console.log(containers[i].trim().slice(1, -1))
        this.containers_id.push(containers_id[i].trim().slice(1, -1))
      }
    })

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


    create_container(create_name, create_image, create_port, int_port, int_ip, vlan_tag) {
      // console.log(create_port)
      this.axios.get('/api/docker/create_container', {
        params: {
          create_name: create_name,
          create_image: create_image,
          create_port: create_port,
        }
      }).then(response => {
        // console.log(response)

        //===========call Jesse's function for advanced configuration========
        // add ovs interfaces and set the ports and ip addresses
        var int_port_list = int_port.split(',')
        var int_ip_list = int_ip.split(',')
        var vlan_tag_list = vlan_tag.split(',')
        var i;
        for (i = 0; i < int_port_list.length; i++) {

          this.axios.get('/api/grpc/ovs_docker_add_port', {

            params: {
              ovs_int: create_name + '_eth' + i,
              int_port: int_port_list[i].trim(),
              int_ip: int_ip_list[i].trim(),
              vlan_tag: vlan_tag_list[i].trim(),
              create_name: create_name,
            }
          }).then(response => {
            // console.log(response)
          })

        }
        //====================end advanced configuration======================


        this.showCreate = false
        this.reload()
      })
    },

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
