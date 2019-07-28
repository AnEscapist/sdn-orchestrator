<template>
  <div class="block btn-group mt-2"
       role="group"
       aria-label="Create VNF"
  >
    <button
      v-if="loading"
      class="btn btn-sample btn-sm"
    >Creating
      <!--            todo: when clicked, show a modal with the just-created vms-->
      <span
        class="spinner-border spinner-border-sm text-warning"
        role="status">
            </span>
    </button>
    <button type="button"
            class="btn btn-sample btn-sm"
            v-b-modal="'vm-create-modal'"
    >
      <span></span>
      <font-awesome-icon :icon="['fas', 'plus-circle']"
                         size=sm
                         color='rgb(255, 255, 255)'/>
      New VNF
    </button>
    <CreateVMModal
      @vm-create-load="onCreateLoad"
      @vm-create-finished="onCreateFinished"
    />
  </div>
</template>

<script>
  import CreateVMModal from '../../../Modals/vnfs/vms/CreateVMModal'

  export default {
    name: "VMCreateButtonGroup",
    components: { CreateVMModal },
    data() {
      return {
        loading: false,
      }
    },
    methods: {
      onCreateLoad(event){
        console.log("creating");
        this.loading = true;
      },
      onCreateFinished(event){
        console.log('create finisehd');
        this.loading = false;
      }
    }
  }
</script>

<style scoped>
  /*.btn-secondary {*/
  /*  background-color: #4a148c;*/
  /*  outline: none;*/
  /*  border: 0;*/
  /*}*/

  .btn-secondary,
  .btn-secondary:active,
  .btn-secondary:hover,
  .btn-secondary:visited,
  .btn-secondary:focus {;
    background-color: #4a148c;
    outline: none;
    border: 0
  }

  /*.btn-secondary:active:focus {*/
  /*  background-color: #4a148c;*/
  /*  outline: none;*/
  /*  border: 0;*/
  /*}*/

  .btn:focus, .btn:active {
    outline: none !important;
    box-shadow: none !important;
  }

  .btn-sample {
    color: #ffffff;
    background-color: #611BBD;
    border: 0;
    outline: none;
  }

  .btn-sample:hover,
  .open {
    color: #ffffff;
    background-color: #49247A;
    border: 0;
    outline: none;
  }

  /* bootstrap button creator: http://blog.koalite.com/bbg/*/
</style>
