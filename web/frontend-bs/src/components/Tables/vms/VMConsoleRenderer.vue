<template>
  <div>
    <button type="button"
            class="btn btn-outline-success btn-sm"
            @click="redirectToConsole(params.data.name)"
            >
      <!--      <h2>{{!!vmSelection}}</h2>-->
<!--      <font-awesome-icon :icon="['fas', 'terminal']"-->
<!--                         size=sm-->
<!--                         color='rgb(255,255,255)'/>-->
      <i class="fas fa-terminal"></i>
      Console
    </button>
  </div>
</template>

<script>
  import Vue from 'vue'
  import {mapActions, mapGetters} from 'vuex'

  // VNC_URL = 'http://10.10.81.51:6080/vnc.html?host=10.10.81.51&port=6080'

    export default Vue.extend({
        name: "VMConsoleRenderer",
        computed: {
          ...mapGetters(['vmWebServerIPV4']),
          vncURL(){
            const vncPort = 6080;
            return `http://${this.vmWebServerIPV4}:${vncPort}/vnc.html?host=${this.vmWebServerIPV4}&port=${vncPort}`
          }
        },
        methods: {
          ...mapActions(['prepareVMConsole']),
          openURLInNewTab(url){
            window.open(url, '_blank');
          },
          redirectToConsole(vm_name){
            this.prepareVMConsole().then(this.openURLInNewTab(this.vncURL))
          }
        }
    })
</script>

<style scoped>

</style>
