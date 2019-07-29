<template>
<div class="content">
  <div class="container-fluid">
    <table width='100%'>
      <tr>
        <td width='91%'>
          <font-awesome-icon :icon="['fas', 'clone']" size=lg color='rgb(0, 0, 0)' /> <strong> Network details - </strong>
          {{net_name}}
        </td>
        <td>
          <router-link to="docker_i">
            <button type="button" id='remove' class="btn btn-danger btn-sm">
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
            <h6>{{id}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>Driver</h6>
          </td>
          <td>
            <h6>{{driver}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>Scope</h6>
          </td>
          <td>
            <h6>{{scope}}</h6>
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
            <h6>Subnet</h6>
          </td>
          <td>
            <h6>{{subnet}}</h6>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>Gateway</h6>
          </td>
          <td>
            <h6>{{gateway}}</h6>
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
  <hr>
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
  name: "DockerNetwork",
  inject: ['reload'],
  data: function() {
    return {
      net_name: '',
      id: '',
      driver: '',
      scope: '',
      created: '',
      subnet: '',
      gateway: '',

      inspect: '',
      showIns: false,
    }


  },
  created() {
    // this.short_id = this.$route.query.short_id
    this.net_id = this.$route.query.net_id

  },
  mounted() {
    this.axios.get('/api/docker/inspect_network', {
      params: {
        network_id: this.net_id
      }
    }).then(response => {
      // console.log(JSON.parse(response.data.result)['return']['Name'])
      var res = JSON.parse(response.data.result)['return']
      this.inspect = res
      this.net_name = res['Name']
      this.id = res['Id']
      this.driver = res['Driver']
      this.scope = res['Scope']
      this.created = res['Created']
      this.subnet = res['IPAM']['Config'][0]['Subnet']
      this.gateway = res['IPAM']['Config'][0]['Gateway']

    })

  },
  methods: {
    showInspect() {
      this.showIns = !this.showIns
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
