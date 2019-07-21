<template>
<div class="content">
  <div class="container-fluid">
    <font-awesome-icon :icon="['fas', 'cogs']" size=lg color='rgb(0, 0, 0)' /> <strong> Actions</strong>

    <hr>
    <button type="button" class="btn btn-success btn-sm" @click="changeStatus('running')">
      <font-awesome-icon :icon="['fas', 'play']" size=sm color='rgb(255,255,255)' />
      Start
    </button>
    <button type="button" class="btn btn-danger btn-sm" @click="changeStatus('exited')">
      <font-awesome-icon :icon="['fas', 'square']" size=sm color='rgb(255, 255, 255)' />
      Stop
    </button>
    <button type="button" class="btn btn-danger btn-sm">
      <font-awesome-icon :icon="['fas', 'skull-crossbones']" size=sm color='rgb(255, 255, 255)' />
      Kill
    </button>
    <button type="button" class="btn btn-primary btn-sm" @click="changeStatus('restart')">
      <font-awesome-icon :icon="['fas', 'sync-alt']" size=sm color='rgb(255, 255, 255)' />
      Restart
    </button>
    <button type="button" class="btn btn-primary btn-sm" @click="changeStatus('paused')">
      <font-awesome-icon :icon="['fas', 'pause']" size=sm color='rgb(255, 255, 255)' />
      Pause
    </button>
    <button type="button" class="btn btn-danger btn-sm">
      <font-awesome-icon :icon="['fas', 'trash-alt']" size=sm color='rgb(255, 255, 255)' />
      Remove
    </button>

  </div>
  <hr>
  <div class="container-fluid">
    <font-awesome-icon :icon="['fas', 'question-circle']" size=lg color='rgb(0, 0, 0)' /> <strong> Container: {{name}}</strong>
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
    {{inspect}}


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
      createTime: '',
      inspect: '',
      showIns: false,
    }


  },
  created() {
    this.name = this.$route.query.name

  },
  mounted() {
    this.axios.get("/api/docker/inspect_container", {
      params: {
        id_name: this.name
      }
    }).then(response => {
      var inspect = JSON.parse(response.data.result)['return']
      // console.log(inspect)
      this.inspect = inspect
      var status = JSON.parse(response.data.result)['return']['State']['Status']
      this.status = status
      // console.log(JSON.parse(response.data.result)['return']['NetworkSettings'].IPAddress)
      var ip = JSON.parse(response.data.result)['return']['NetworkSettings'].IPAddress
      this.ip = ip
      var id = JSON.parse(response.data.result)['return']['Id']
      this.id = id
      var createTime = JSON.parse(response.data.result)['return']['Created']
      this.createTime = createTime
    });
  },
  methods: {
    changeStatus(change_to) {
      this.axios.get("/api/docker/change_status", {
        params: {
          id_name: this.name,
          change_to: change_to
        }
      }).then(response => {
        var res = JSON.parse(response.data.result)['return']
        var status = res.substring(res.indexOf('[') + 1, res.indexOf(']'))

        //after hit the button, re-render the status and ip address
        this.axios.get("/api/docker/inspect_container", {
          params: {
            id_name: this.name
          }
        }).then(response => {
          var status = JSON.parse(response.data.result)['return']['State']['Status']
          this.status = status
          // console.log(JSON.parse(response.data.result)['return']['NetworkSettings'].IPAddress)
          var ip = JSON.parse(response.data.result)['return']['NetworkSettings'].IPAddress
          this.ip = ip
        });

      });

    },
    showInspect() {
      this.showIns = !this.showIns;
    }
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
