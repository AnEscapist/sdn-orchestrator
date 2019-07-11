<template>
  <div class="dashboard">
      <div class="content">
          <div class='header'>
             <strong>Endpoint info</strong><font-awesome-icon :icon="['fas', 'tachometer-alt']" size=lg pull='left' color="black"/>
          </div>
          <div class='info'>
             <strong>Endpoint: </strong>{{endpoint}} - get from local json data.
         </div>
          <div class='info'>
             <strong>URL</strong>
         </div>
          <div class='info'>
             <strong>Tags</strong>
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
    data() {
        return {
            endpoint: '',
            content: ''
        };
    }
    mounted() {
        this.axios.get("../manifest.json").then(response => {
            console.log(response.data)
            this.endpoint = response.data.name
        });
        this.axios.post("http://api.komavideo.com/news/list").then(body => {
            this.content = body.data[0].title;
        })
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
    background: white;
    margin-left: 220px;
    margin-right: 20px;
}


</style>
