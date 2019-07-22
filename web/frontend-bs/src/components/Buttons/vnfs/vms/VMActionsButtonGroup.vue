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
      id="vm-remove-modal">
      <div>
      Are you sure you want to remove the VNFs below?
      <br/>
      <strong>This operation cannot be undone.</strong>
      </div>
    </b-modal>
<!--        <b-modal-->
<!--          id="vm-remove-modal">-->
<!--          <div>-->
<!--            Some text-->
<!--          </div>-->
<!--        </b-modal>-->
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

</style>
