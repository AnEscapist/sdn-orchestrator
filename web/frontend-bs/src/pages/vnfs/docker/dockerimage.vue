<template>
<div class="content">
  <div class="container-fluid">
    <table width='100%'>
      <tr>
        <td width='91%'>
          <font-awesome-icon :icon="['fas', 'clone']" size=lg color='rgb(0, 0, 0)' /> <strong> Image details - </strong>
          {{name}}
        </td>
        <td>
          <router-link to="docker_i">
            <button type="button" id='remove' class="btn btn-danger btn-sm" @click='removeImage()'>
              <font-awesome-icon :icon="['fas', 'trash-alt']" size=sm color='rgb(255, 255, 255)' />
              Remove
            </button>
          </router-link>
        </td>
      </tr>
    </table>
    <hr>


    <div>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>ID</h6>
          </td>
          <td>
            <h6>{{image_id}}</h6>
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
            <h6>{{created}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>Size</h6>
          </td>
          <td>
            <h6>{{size}}MB</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>Build</h6>
          </td>
          <td>
            <h6>Docker {{dockerVersion}} on {{os}}, {{architecture}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>CMD</h6>
          </td>
          <td>
            <h6>{{cmd}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>ENV</h6>
          </td>
          <td>
            <h6>{{env}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table>
        <tr id='containerLinks'>
          <!-- <button type="button" class="btn btn-link">
            <td>
              <font-awesome-icon :icon="['fas', 'trash-alt']" size=sm coler="#1b7fbd" />
              <font size='2px'> Delete</font>
            </td>
          </button> -->
          <button type="button" class="btn btn-link" @click='showInspect()'>
            <td>
              <font-awesome-icon :icon="['fas', 'info-circle']" size=sm coler="#1b7fbd" />
              <font size='2px'> Inspect</font>
            </td>
          </button>
        </tr>
      </table>
    </div>


  </div>

  <div class="container-fluid" v-show="showIns">
    <font-awesome-icon :icon="['fas', 'info-circle']" size=lg color='rgb(0, 0, 0)' /> <strong> Inspect</strong>
    <hr>
    <pre><span class="inner-pre">{{inspect}}</span></pre>
  </div>
</div>
</template>

<script>
import Card from '@/components/Cards/Card.vue'
export default {
  name: "DockerImage",
  data: function() {
    return {
      inspect: '',
      image_id: '',
      created: '',
      size: '',
      dockerVersion: '',
      os: '',
      architecture: '',
      cmd: '',
      env: '',

      showIns: false,
    }


  },
  created() {
    this.name = this.$route.query.name

  },
  mounted() {

    this.axios.get('/api/docker/inspect_image', {
      params: {
        name: this.name
      }
    }).then(response => {
      var inspect = JSON.parse(response.data.result)['return']
      this.inspect = inspect
      this.image_id = inspect['Id']
      this.created = inspect['Created']
      this.size = (parseFloat(inspect['Size']) / 1000000).toFixed(1)
      this.dockerVersion = inspect['DockerVersion']
      this.os = inspect['Os']
      this.architecture = inspect['Architecture']
      this.cmd = inspect['Config']['Cmd'][0]
      this.env = inspect['Config']['Env'][0]
    })

  },
  methods: {
    showInspect() {
      this.showIns = !this.showIns
    },
    removeImage() {
      this.axios.get('/api/docker/remove_image', {
        params: {
          name: this.name
        }
      }).then(response => {
        // console.log(response)
      })
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
