<template>
  <div class="block btn-group mt-2"
       role="group"
       aria-label="Create VNF">
    <button class="btn btn-secondary btn-sm">Creating
      <!--            todo: when clicked, show a modal with the just-created vms-->
      <span
        class="spinner-border spinner-border-sm text-warning"
        role="status">
            </span>
    </button>
    <button type="button"
            v-b-modal="'vm-create-modal'"
            class="btn btn-secondary btn-sm"
    >
      <span></span>
      <font-awesome-icon :icon="['fas', 'plus-circle']"
                         size=sm
                         color='rgb(255, 255, 255)'/>
      New VNF
    </button>
  </div>
</template>

<script>
  export default {
    name: "VMCreateButtonGroup"
  }
</script>

<style scoped>
  /*.btn-secondary {*/
  /*  background-color: #4a148c;*/
  /*  outline: none;*/
  /*  border: 0;*/
  /*}*/

  .btn-secondary,
  .btn-secondary:hover,
  .btn-secondary:active,
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
</style>
