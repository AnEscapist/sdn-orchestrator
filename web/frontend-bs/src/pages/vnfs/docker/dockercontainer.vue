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
    <button type="button" id='kill' class="btn btn-danger btn-sm">
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
    <button type="button" id='remove' class="btn btn-danger btn-sm">
      <font-awesome-icon :icon="['fas', 'trash-alt']" size=sm color='rgb(255, 255, 255)' />
      Remove
    </button>

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
          <button type="button" class="btn btn-link">
            <td>
              <font-awesome-icon :icon="['fas', 'file-alt']" size=sm coler="#1b7fbd" />
              <font size='2px'> Logs</font>
            </td>
          </button>
          <button type="button" class="btn btn-link" @click='showInspect()'>
            <td>
              <font-awesome-icon :icon="['fas', 'info-circle']" size=sm coler="#1b7fbd" />
              <font size='2px'> Inspect</font>
            </td>
          </button>
          <button type="button" class="btn btn-link">
            <td>
              <font-awesome-icon :icon="['fas', 'chart-area']" size=sm coler="#1b7fbd" />
              <font size='2px'> Stats</font>
            </td>
          </button>
          <button type="button" class="btn btn-link">
            <td>
              <font-awesome-icon :icon="['fas', 'terminal']" size=sm coler="#1b7fbd" />
              <font size='2px'> Console</font>
            </td>
          </button>
        </tr>
      </table>
    </div>
    <div>
    </div>
  </div>

  <div class="container-fluid" v-if="showIns == true">
    <font-awesome-icon :icon="['fas', 'info-circle']" size=lg color='rgb(0, 0, 0)' /> <strong> Inspect</strong>
    <hr>
    <pre><span class="inner-pre">{{inspect}}</span></pre>
  </div>
</div>
</template>

<script>
import Card from '@/components/Cards/Card.vue'
export default {
  name: "DockerContainer",
  data: function() {
    return {
      status: '',
      ip: '',
      id: '',
      name: '',
      createTime: '',
      inspect: '',
      showIns: false,
      showEdit: true,
      newName: '',
    }


  },
  created() {
    this.short_id = this.$route.query.short_id

  },
  mounted() {
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

  },
  methods: {
    changeStatus(change_to) {
      this.axios.get("/api/docker/change_status", {
        params: {
          id_name: this.id,
          change_to: change_to
        }
      }).then(response => {
        var res = JSON.parse(response.data.result)['return']
        var status = res.substring(res.indexOf('[') + 1, res.indexOf(']'))

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

      });

    },
    showInspect() {
      this.showIns = !this.showIns;
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

    setBtn(status){
        if (status == 'exited'){
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

        }
        else if (status == 'running') {
            document.getElementById("start").removeAttribute("disabled");
            document.getElementById("stop").removeAttribute("disabled");
            document.getElementById("kill").removeAttribute("disabled");
            document.getElementById("restart").removeAttribute("disabled");
            document.getElementById("pause").removeAttribute("disabled");

            document.getElementById("start").setAttribute("disabled", true);
            document.getElementById("restart").setAttribute("disabled", true);
            document.getElementById("remove").setAttribute("disabled", true);
        }
        else if (status == 'paused') {
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
  height: 18px;
  /* background-color: red; */
  background-color: rgb(247, 247, 247);
  border: none;
  border-bottom: 1px solid rgb(89, 89, 89);
  padding-left: 3px;
  margin-bottom: 0px;
}

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
</style>
