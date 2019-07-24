<template>
<div class="content">
  <div class="container-fluid">
    <table width='100%'>
      <tr>
        <td width='91%'>
          <font-awesome-icon :icon="['fas', 'cubes']" size=lg color='rgb(0, 0, 0)' /> <strong> Volume details - </strong>
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
            <h6>{{name}}</h6>
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
            <h6>Mountpoint</h6>
          </td>
          <td>
            <h6>{{mountPoint}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>driver</h6>
          </td>
          <td>
            <h6>{{driver}}</h6>
          </td>
        </tr>
      </table>
      <hr>

    </div>

  </div>
</div>
</template>

<script>
import Card from '@/components/Cards/Card.vue'
export default {
  name: "DockerVolume",

  data: function() {
    return {
        created: '',
        mountPoint: '',
        driver: '',
    }


  },
  created() {
    this.name = this.$route.query.name

  },
  mounted() {

    this.axios.get('/api/docker/inspect_volume', {
      params: {
        name: this.name
      }
    }).then(response => {
      var inspect = JSON.parse(response.data.result)['return']
      this.inspect = inspect
      this.created = inspect['CreatedAt'].slice(0, -1).split('T').join(' / ')
      this.mountPoint = inspect['Mountpoint']
      this.driver = inspect['Driver']
    })

  },
  methods: {}

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
