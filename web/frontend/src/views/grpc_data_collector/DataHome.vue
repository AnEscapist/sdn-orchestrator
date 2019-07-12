<template>
  <div class="data-home">

      <div id="nav">

        <router-link to="/login">Login</router-link> |
        <router-link to="/docker">Docker</router-link> |
        <router-link to="/data-collect">Data collector</router-link>
        <DSidebar></DSidebar>

      </div>
      <div class="content">
          <div class='header'>
             <strong>Home</strong><font-awesome-icon :icon="['fas', 'home']" size=lg pull='left' color="black"/>
          </div>
          <br>
          <div class='info'>
              <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)'/>
             <strong>Data Collector on uCPE (IP address) {{endpoint}}</strong>
             <span class="badge badge-success">Running</span>
             <hr>

         </div>
         <br>
         <div class='info'>
             <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)'/>
            <strong>Data Collector on uCPE (IP address) </strong>
            <span class="badge badge-danger">Exited</span>
            <hr>

        </div>
        <br>
        <div class='info'>
            <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)'/>
           <strong>Data Collector on uCPE (IP address) </strong>
           <span class="badge badge-warning">Paused</span>
           <hr>

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
export default class DataHome extends Vue {
    name: 'data-home'
    data() {
        return {
            endpoint: '',
            content: ''
        };
    }
    mounted() {
        this.axios.get("/api/data-collect/get_cpu_count").then(response => {
            // console.log(typeof (response.data.result))
            // var obj = JSON.parse(response.data.result)
            // console.log('obj', obj['return'])
            this.endpoint = response.data.result
        });
    }

}
</script>

<style lang="css" scoped>
.header{
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(226, 226, 226);
    text-align: left;

}

.content{
    border: 1px, solid rgb(0, 0, 0);
    height: auto;
    margin-left: 220px;
    margin-right: 20px;
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

.ucpe{
    font-size: 15px;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(240, 240, 240);
    text-align: left;

}

.ucpe-info{
    width: 100px;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    background: rgb(226, 226, 226);
    text-align: left;

}


</style>
