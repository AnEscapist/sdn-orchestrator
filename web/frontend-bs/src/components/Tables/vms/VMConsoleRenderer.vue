<template>
  <div>
    <button type="button"
            :disabled="params.data.state !== 'Running'"
            class="btn btn-primary btn-sm"
            @click.stop="redirectToConsole(params.data.name)"
    >
      <!--            todo: figure out color conflict with pause-->
      <!--      <h2>{{!!vmSelection}}</h2>-->
      <!--      <font-awesome-icon :icon="['fas', 'terminal']"-->
      <!--                         size=sm-->
      <!--                         color='rgb(255,255,255)'/>-->
      <span v-if="!loading">
      <i class="fas fa-terminal"></i>
      </span>
      <span v-if="loading"
           class="spinner-border spinner-border-sm text-warning"
           role="status">
      </span>
      {{params.data.name}}
    </button>
  </div>
</template>

<script>
  import Vue from 'vue'
  import { mapActions, mapGetters } from 'vuex'

  // VNC_URL = 'http://10.10.81.51:6080/vnc.html?host=10.10.81.51&port=6080'

  export default Vue.extend({
    name: "VMConsoleRenderer",
    data() {
      return {
        loading: false
      }
    },
    computed: {
      ...mapGetters(['vmWebServerIPV4']),
      vncURL() {
        const vncPort = 6080;
        return `http://${this.vmWebServerIPV4}:${vncPort}/vnc.html?host=${this.vmWebServerIPV4}&port=${vncPort}`
      },
    },
    methods: {
      ...mapActions(['prepareVMConsole']),
      openURLInNewTab(url) {
        window.open(url, '_blank');
      },
      redirectToConsole(vm_name) {
        new Promise((resolve) => {
          this.loading = true;
          const success = true;
          return resolve({ success });
        }).then(() => {
          this.prepareVMConsole(vm_name).catch(err => console.log(err)).then(() => {
            this.openURLInNewTab(this.vncURL)
          }).then(() => this.loading=false);
        })
      }
    }
  })
</script>

<style scoped>
  .btn:focus, .btn:active:focus, .btn.active:focus, .btn.focus, .btn:active.focus, .btn.active.focus {
    outline: none !important;
    box-shadow: none !important;
  }
</style>
