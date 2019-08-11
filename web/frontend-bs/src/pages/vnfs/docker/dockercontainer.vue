<template>
<div class="content">
  <div class="container-fluid">
    <font-awesome-icon :icon="['fas', 'cogs']" size=lg color='rgb(0, 0, 0)' /> <strong> Actions</strong>

    <hr>
    <button type="button" id='start' class="btn btn-success btn-sm" @click="changeStatus('running')">
      <font-awesome-icon :icon="['fas', 'play']" size=sm color='rgb(255,255,255)' />
      Start
    </button>
    <button type="button" id='stop' class="btn btn-danger btn-sm" @click="changeStatus('exited')">
      <font-awesome-icon :icon="['fas', 'square']" size=sm color='rgb(255, 255, 255)' />
      Stop
    </button>
    <button type="button" id='kill' class="btn btn-danger btn-sm" @click='killContainer()'>
      <font-awesome-icon :icon="['fas', 'skull-crossbones']" size=sm color='rgb(255, 255, 255)' />
      Kill
    </button>
    <button type="button" id='restart' class="btn btn-primary btn-sm" @click="changeStatus('restart')">
      <font-awesome-icon :icon="['fas', 'sync-alt']" size=sm color='rgb(255, 255, 255)' />
      Restart
    </button>
    <button type="button" id='pause' class="btn btn-primary btn-sm" @click="changeStatus('paused')">
      <font-awesome-icon :icon="['fas', 'pause']" size=sm color='rgb(255, 255, 255)' />
      Pause
    </button>

    <router-link to="docker_c">
      <button type="button" id='remove' class="btn btn-danger btn-sm" @click='removeContainer()'>
        <font-awesome-icon :icon="['fas', 'trash-alt']" size=sm color='rgb(255, 255, 255)' />
        Remove
      </button>
    </router-link>


  </div>
  <hr>
  <div class="container-fluid">
    <font-awesome-icon :icon="['fas', 'question-circle']" size=lg color='rgb(0, 0, 0)' />
    <strong> Container: {{name}} </strong>
    <button class="renameBtn" @click="showEdit = !showEdit">
      <font-awesome-icon :icon="['fas', 'edit']" size=sm color='#1b7fbd' v-if='showEdit' />
    </button>
    <span v-if='!showEdit'>
      <font-awesome-icon :icon="['fas', 'chevron-right']" size=sm color='rgb(0, 0, 0)' />
      <input type="text" placeholder="new name" v-model='newName' @keyup.enter='renameContainer(newName)'>
    </span>
    <hr>
    <div>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>ID</h6>
          </td>
          <td>
            <h6>{{id}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>IP address</h6>
          </td>
          <td v-if="ip == ''">
            <h6> - </h6>
          </td>
          <td v-else>
            <h6>{{ip}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>Status</h6>
          </td>
          <td v-if="status == 'running' ">
            <h5><span class="badge badge-success">{{status}}</span></h5>
          </td>
          <td v-else-if="status == 'exited' ">
            <h5><span class="badge badge-danger">{{status}}</span></h5>
          </td>
          <td v-else>
            <h5><span class="badge badge-primary">{{status}}</span></h5>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>Created</h6>
          </td>
          <td>
            <h6>{{createTime}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table>
        <tr id='containerLinks'>
          <!-- <button type="button" class="btn btn-link" @click='showOVSConfig()'>
            <td>
              <font-awesome-icon :icon="['fas', 'cog']" size=sm coler="#1b7fbd" />
              <font size='2px'> OVS config</font>
            </td>
          </button> -->
          <button type="button" class="btn btn-link" @click='showInspect()'>
            <td>
              <font-awesome-icon :icon="['fas', 'info-circle']" size=sm coler="#1b7fbd" />
              <font size='2px'> Inspect</font>
            </td>
          </button>
          <button type="button" class="btn btn-link" @click='showStatistic()'>
            <td>
              <font-awesome-icon :icon="['fas', 'chart-area']" size=sm coler="#1b7fbd" />
              <font size='2px'> Stats</font>
            </td>
          </button>

          <button type="button" class="btn btn-link" @click='goConsole(id)'>
            <!-- <router-link target="_blank" :to="{ path: 'consolecontainer', query: {short_id: this.short_id} }"> -->
            <td>
              <font-awesome-icon :icon="['fas', 'terminal']" size=sm coler="#1b7fbd" />
              <font size='2px'> Console</font>
            </td>
            <!-- </router-link> -->
          </button>
          <button v-show="port_listening=='yes'" type="button" class="btn btn-danger btn-xs" @click='stopConsole()' color='red'>
            <!-- <router-link target="_blank" :to="{ path: 'consolecontainer', query: {short_id: this.short_id} }"> -->
            <td>
              <font-awesome-icon :icon="['far', 'times-circle']" size=1x />
              <!-- <font size='1px'> stop console</font> -->
            </td>
            <!-- </router-link> -->
          </button>

          <button type="button" class="btn btn-link" @click='showCommit()'>
            <td>
              <font-awesome-icon :icon="['fas', 'save']" size=sm coler="#1b7fbd" />
              <font size='2px'> Commit</font>
            </td>
          </button>


        </tr>
      </table>



    </div>
    <div>
    </div>
  </div>
  <br>

  <!-- <div id="console">
  </div> -->



  <div class="container-fluid" v-show="showIns">
    <font-awesome-icon :icon="['fas', 'info-circle']" size=lg color='rgb(0, 0, 0)' /> <strong> Inspect</strong>
    <hr>
    <pre><span class="inner-pre">{{inspect}}</span></pre>
  </div>

  <div class="container-fluid" v-show="showStats">
    <font-awesome-icon :icon="['fas', 'chart-area']" size=lg color='rgb(0, 0, 0)' /> <strong> Stats</strong>
    <hr>
    <pre><span class="inner-pre">{{stats}}</span></pre>
  </div>

  <div class="container-fluid" v-show="showCom">
    <font-awesome-icon :icon="['fas', 'save']" size=lg color='rgb(0, 0, 0)' /> <strong> Commit</strong>
    <hr>
    <table width='100%'>
      <br>
      <tr>
        <td width='20%'>
          <form class="form-inline">
            <strong style="font-size:15px">Image: &nbsp</strong>
            <input type="text" placeholder="e.g. repo:tag" v-model='commit_img'>
          </form>
        </td>
        <td width='50%'></td>

      </tr>
    </table width='100%'>
    <table>
      <tr>
        <td width='43%'></td>
        <td width='42%'></td>
        <td>
          <button type="button" class="btn btn-secondary btn-sm" @click='showCom = false'>
            Cancel
          </button>
        </td>
        <td width='10%'>
          <button type="button" class="btn btn-primary btn-sm" @click="commit(commit_img)">
            <font-awesome-icon :icon="['fas', 'cloud-download-alt']" size=sm /> <strong style="font-size:13px"> Commit</strong>
          </button>
        </td>
      </tr>
    </table>
  </div>

</div>
</template>

<script>
import Card from '@/components/Cards/Card.vue'
export default {
  name: "DockerContainer",
  inject: ['reload'],
  data: function() {
    return {
      status: '',
      ip: '',
      id: '',
      name: '',
      createTime: '',
      inspect: '',
      stats: '',
      showOVSCon: false,
      showIns: false,
      showEdit: true,
      showStats: false,
      showCom: false,
      newName: '',
      port_listening: 'no',

      int_port: '',
      int_ip: '',

      commit_img: '',

    }


  },
  created() {
    this.short_id = this.$route.query.short_id

  },
  mounted() {
    this.axios.get('/api/docker/check_port').then(response => {
      // console.log(typeof(response.data))
      this.port_listening = response.data
    })

    this.axios.get("/api/docker/inspect_container", {
      params: {
        id_name: this.short_id
      }
    }).then(response => {
      var inspect = JSON.parse(response.data.result)['return']
      this.inspect = inspect
      this.status = inspect['State']['Status']
      this.setBtn(this.status)
      this.ip = inspect['NetworkSettings'].IPAddress
      this.id = inspect['Id']
      this.name = inspect['Name'].slice(1, inspect['Name'].legth)
      this.createTime = inspect['Created']
    });

    this.axios.get('/api/docker/container_stats', {
      params: {
        id_name: this.short_id
      }
    }).then(response => {
      // console.log(response.data.result)
      var stats = JSON.parse(response.data.result)['return']
      this.stats = stats
    })

  },
  methods: {
    changeStatus(change_to) {
      this.axios.get('/api/docker/kill_port').then(response => {

        this.axios.get("/api/docker/change_status", {
          params: {
            id_name: this.short_id,
            change_to: change_to
          }
        }).then(response => {
          // console.log(response)
          var res = JSON.parse(response.data.result)['return']
          var status = res.substring(res.indexOf('[') + 1, res.indexOf(']'))

          this.update()

        });

      })


    },
    showOVSConfig() {
      this.showIns = false;
      this.showStats = false;
      this.showCom = false;
      this.showOVSCon = !this.showOVSCon;
    },
    showInspect() {
      this.showStats = false;
      this.showOVSCon = false;
      this.showCom = false;
      this.showIns = !this.showIns;
    },
    showStatistic() {
      this.showIns = false;
      this.showOVSCon = false;
      this.showCom = false;
      this.showStats = !this.showStats
    },
    showCommit() {
      this.showIns = false;
      this.showOVSCon = false;
      this.showStats = false;
      this.showCom = !this.showCom
    },

    renameContainer(newName) {
      this.showEdit = !this.showEdit
      var tmp = this.name
      this.axios.get('/api/docker/rename_container', {
        params: {
          id_name: this.id,
          newName: newName
        }
      }).then(response => {
        var res = JSON.parse(response.data.result)['return']
        if (res) {
          this.name = JSON.parse(response.data.result)['return']
        } else {
          this.name = tmp
        }
      })
    },

    removeContainer() {
      this.axios.get('/api/docker/kill_port').then(response => {

        this.axios.get('/api/docker/remove_container', {
          params: {
            id_name: this.id,
          }
        }).then(response => {
          // console.log('container name', this.name)
          this.axios.get('/api/grpc/ovs_docker_del_port', {
            params: {
              container: this.name,
            }
          }).then(response => {
            // console.log(response)
          })
          // console.log(this.id)
          // console.log(response.data.result)
        })

      })

    },

    killContainer() {

      this.axios.get('/api/docker/kill_port').then(response => {

        this.axios.get('/api/docker/kill_container', {
          params: {
            id_name: this.id,
          }
        }).then(response => {
          this.update()

        })

      })

    },

    update() {
      //after hit the button, re-render the status and ip address
      this.axios.get("/api/docker/inspect_container", {
        params: {
          id_name: this.id
        }
      }).then(response => {
        var inspect = JSON.parse(response.data.result)['return']
        // inspect = JSON.parse(inspect)
        var status = inspect['State']['Status']
        this.status = status
        var ip = inspect['NetworkSettings'].IPAddress
        this.ip = ip
        this.setBtn(status)

      });
    },

    goConsole(id) {
      this.port_listening = 'yes'

      this.axios.get('/api/docker/kill_port').then(response => {
        // window.open(url, '_blank')
        // console.log(response)
        this.axios.get('/api/docker/console_container', {
          params: {
            container_id: id
          },
        }).then(response => {
          // console.log('response', response)
          // this.reload()
        })

      })



      // var path = '/#/ucpe/123/vnfs/dockercontainer?short_id=' + this.short_id
      // var path = 'file:///home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/index.html'
      // var path = 'https://www.google.com'
      // var path = 'file:///home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/index.html'
      // var path = 'file:///home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/index.html'
      // window.open(path)

      // console.log(id)
      // document.getElementById("console").innerHTML = '<object type="text/html" data="hello.html" ></object>';


    },
    stopConsole() {
      this.axios.get('/api/docker/kill_port').then(response => {
        // console.log(response)
        this.reload()
      })
    },

    commit(commit_img) {
      var repo;
      var tag;
      if (commit_img.includes(':')) {
        repo = commit_img.split(':')[0]
        tag = commit_img.split(':')[1]
      } else {
        repo = commit_img
        tag = 'latest'
      }
      this.axios.get('/api/docker/commit', {
        params: {
          id_name: this.name,
          repo: repo,
          tag: tag
        }
      }).then(response => {
        // console.log(response)
        this.showCom = false
      })
    },

    setBtn(status) {
      if (status == 'exited') {
        document.getElementById("start").removeAttribute("disabled");
        document.getElementById("stop").removeAttribute("disabled");
        document.getElementById("kill").removeAttribute("disabled");
        document.getElementById("restart").removeAttribute("disabled");
        document.getElementById("pause").removeAttribute("disabled");
        document.getElementById("remove").removeAttribute("disabled");

        document.getElementById("stop").setAttribute("disabled", true);
        document.getElementById("kill").setAttribute("disabled", true);
        document.getElementById("restart").setAttribute("disabled", true);
        document.getElementById("pause").setAttribute("disabled", true);

      } else if (status == 'running') {
        document.getElementById("start").removeAttribute("disabled");
        document.getElementById("stop").removeAttribute("disabled");
        document.getElementById("kill").removeAttribute("disabled");
        document.getElementById("restart").removeAttribute("disabled");
        document.getElementById("pause").removeAttribute("disabled");

        document.getElementById("start").setAttribute("disabled", true);
        document.getElementById("restart").setAttribute("disabled", true);
        document.getElementById("remove").setAttribute("disabled", true);
      } else if (status == 'paused') {
        document.getElementById("start").removeAttribute("disabled");
        document.getElementById("stop").removeAttribute("disabled");
        document.getElementById("kill").removeAttribute("disabled");
        document.getElementById("restart").removeAttribute("disabled");
        document.getElementById("pause").removeAttribute("disabled");

        document.getElementById("start").setAttribute("disabled", true);
        document.getElementById("pause").setAttribute("disabled", true);
        document.getElementById("remove").setAttribute("disabled", true);

      }
    },

  }

}
</script>

<style scoped>
.container-fluid {
  border: 1px solid rgb(208, 208, 208);
  padding-top: 15px;
  padding-bottom: 13px;
}

a {
  color: #1b7fbd;
}

font {
  font-weight: bold;
}

input {

  border: 2px solid rgb(200, 200, 200);
  border-radius: 4px;
  padding-left: 8px;
}

/* input {
  height: 18px;
  background-color: rgb(247, 247, 247);
  border: none;
  border-bottom: 1px solid rgb(89, 89, 89);
  padding-left: 3px;
  margin-bottom: 0px;
} */

.renameBtn {
  background-color: white;
  border: 0px solid black;
  padding: 0;
}

.renameBtn:active {
  outline: none;
  padding: 0;
}

.inner-pre {
  font-family: Arial, sans-serif;
  font-weight: bold;
  font-size: 12px;
}

#console {
  background-color: red;
}

#textR {
  text-align: right;
}

h6 {
  text-transform: none;
}

hr {
  padding-top: 0;
  margin-top: 0px;

}

.btn-group-xs>.btn,
.btn-xs {
  padding: .25rem .4rem;
  font-size: .875rem;
  line-height: .5;
  border-radius: .2rem;
}
</style>
