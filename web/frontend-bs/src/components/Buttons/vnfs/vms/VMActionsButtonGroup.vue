<template>
  <div class="block btn-group mt-2"
       role="group"
       aria-label="State Changes">
    <button type="button"
            class="btn btn-success btn-sm"
            :disabled="!vmAtLeastOneSelected"
            @click="startSelectedVMs">
<!--      <h2>{{!!vmSelection}}</h2>-->
      <font-awesome-icon :icon="['fas', 'play']"
                         size=sm
                         color='rgb(255,255,255)'/>
      Start
    </button>
    <!--      <button type="button" class="btn btn-danger btn-sm" @click="changeStatus('exited')">-->
    <!--        <font-awesome-icon :icon="['fas', 'square']" size=sm color='rgb(255, 255, 255)' />-->
    <!--        Stop-->
    <!--      </button>-->
    <button type="button"
            class="btn btn-primary btn-sm"
            :disabled="!vmAtLeastOneSelected"
            @click="pauseSelectedVMs">
      <font-awesome-icon :icon="['fas', 'pause']"
                         size=sm
                         color='rgb(255, 255, 255)'/>
      Pause
    </button>
    <button type="button"
            class="btn btn-danger btn-sm"
            :disabled="!vmAtLeastOneSelected"
            @click="killSelectedVMs">
      <font-awesome-icon :icon="['fas', 'skull-crossbones']"
                         size=sm
                         color='rgb(255, 255, 255)'/>
      Kill
    </button>
    <!--      <button type="button" class="btn btn-primary btn-sm" @click="changeStatus('restart')">-->
    <!--        <font-awesome-icon :icon="['fas', 'sync-alt']" size=sm color='rgb(255, 255, 255)' />-->
    <!--        Restart-->
    <!--      </button>-->
    <button type="button"
            class="btn btn-dark btn-sm"
            :disabled="!vmAtLeastOneSelected"
            v-b-modal="'vm-remove-modal'"
    >
      <font-awesome-icon :icon="['fas', 'trash-alt']"
                         size=sm
                         color='rgb(255, 255, 255)'/>
      Remove
    </button>
    <!-- The modal -->
    <b-modal
      ok-variant="danger"
      ok-title="Proceed"
      @ok="deleteSelectedVMs"
      id="vm-remove-modal">
      <div>
        <strong>Are you sure you would like to proceed with removal of the VNFs below?</strong>
        <ul>
          <li v-for="vmName in vmSelection">{{vmName}}</li>
        </ul>
      </div>
      <strong class="text-danger">This operation cannot be undone.</strong>
    </b-modal>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex';

  export default {
    name: "VMActionsButtonGroup",
    computed: {
      ...mapGetters([
        'vnfList', 'vnfCount', 'vmList', 'vmInfo', 'vmSelection', 'vmFilterText', 'vmStateFromName', 'vmAtLeastOneSelected'
      ])
    },
    methods: {
      ...mapActions([
        'updateVMSelection', 'updateVMFilterText', 'startSelectedVMs', 'pauseSelectedVMs', 'killSelectedVMs', 'deleteSelectedVMs'
      ]),
    }
  }
</script>

<style scoped>
  .btn:focus, .btn:active:focus, .btn.active:focus, .btn.focus, .btn:active.focus, .btn.active.focus {
    outline: none !important;
    box-shadow: none !important;
  }
</style>
