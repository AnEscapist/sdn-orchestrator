<template>
  <div class="data-dashboard">
      <div id="nav">
        <!-- <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> | -->

        <router-link to="/login">Login</router-link> |
        <router-link to="/docker">Docker</router-link>
        <router-link to="/data-collect">Data collector</router-link>
        <DSidebar></DSidebar>

      </div>

      <div class="content">

          <div class='header'>

             <strong>Endpoint info</strong><font-awesome-icon :icon="['fas', 'tachometer-alt']" size=lg pull='left' color="black"/>
          </div>
          <div class='info'>
              <table>
                  <tr>
                      <td width='200px'><strong>Endpoint</strong></td>
                      <td>local <font-awesome-icon :icon="['fas', 'microchip']" size=sm color='rgb(111, 111, 111)'/> 8
                           <font-awesome-icon :icon="['fas', 'memory']" size=sm color='rgb(111, 111, 111)'/> 16.7GB
                           - Standalone 18.09.5
                      </td>
                  </tr>
              </table>
         </div>
          <div class='info'>
              <table>
                  <tr>
                      <td width='200px'>
                          <strong>URL </strong>
                          <font-awesome-icon :icon="['fas', 'link']" size=sm color='rgb(111, 111, 111)'/>
                      </td>
                      <td>/var/run/docker.sock</td>
                  </tr>
              </table>
         </div>
          <div class='info'>
              <table>
                  <tr>
                      <td width='200px'>
                          <strong>Tags </strong>
                          <font-awesome-icon :icon="['fas', 'tags']" size=sm color='rgb(111, 111, 111)' flip='horizontal' />
                      </td>
                      <td>-</td>
                  </tr>
                  {{endpoint}}
              </table>
         </div>
         <div class='info'>
            <strong>Content: </strong>{{content}} - get from remote api
        </div>
      </div>

  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import DSidebar from '@/components/DSidebar.vue';

@Component({
  components: {
      DSidebar,
  },
})
export default class Dashboard extends Vue {
    name: 'data-dashboard'
    data() {
        return {
            endpoint: '',
            content: ''
        };
    }
    mounted() {
        this.axios.get("/api/data-collect/dashboard").then(response => {

            console.log(typeof(response.data.result))
            var obj = JSON.parse(response.data.result)
            console.log('obj', obj['return'])
            this.endpoint = response.data.result
        });
    }
}
</script>

<style lang="css" scoped>

.header{
    background: red;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(226, 226, 226);
    text-align: left;

}
.info{
    font-size: 15px;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(240, 240, 240);
    text-align: left;

}
.content{
    border: 1px, solid rgb(0, 0, 0);
    height: auto;
    background: red;
    margin-left: 220px;
    margin-right: 20px;
}


</style>
