<template>
  <div class="dockerhome">

      <div id="nav">

        <router-link to="/login">Login</router-link> |
        <router-link to="/docker">Docker</router-link>
        <DSidebar></DSidebar>

      </div>
      <div class="content">
          <div class='header'>
             <strong>Home</strong><font-awesome-icon :icon="['fas', 'home']" size=lg pull='left' color="black"/>
          </div>
          <br>
          <div class='info'>
              <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)'/>
             <strong>Docker on uCPE (IP address) </strong>
             <hr>
             <ul>
                 <li>a</li>
                 <li>b</li>
             </ul>
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
export default class DockerHome extends Vue {
    name: 'dockerhome'
    data() {
        return {
            endpoint: '',
            content: ''
        };
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
