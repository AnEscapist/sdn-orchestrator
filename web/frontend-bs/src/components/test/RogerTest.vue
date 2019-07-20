<template>
  <div>
    <card>
      <h1>Roger's Playground</h1>
      <h2>VNF Count: {{vnfCount}}</h2>
      <h2>VNF List: {{vnfList}}</h2>
      <h2>VM List: {{vmList}}</h2>
      <h2>VM Info: {{vmInfo}}</h2>
      <VMTableOld></VMTableOld>
      <VMTableNew></VMTableNew>
    </card>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import VMTableOld from '../Tables/vms/VMTableOld'
  import VMTableNew from '../Tables/vms/VMTableNew'

  export default {
    name: "RogerTest",
    components: {
      VMTableOld, VMTableNew
    },
   created() {
      this.$store.dispatch('updateContainerList');
      this.$store.dispatch('updateVMList');
      this.$store.dispatch('updateVMInfo');
    },
    computed: {
      ...mapGetters([
        'vnfList', 'vnfCount', 'vmList', 'vmInfo'
      ])
    },
    methods: {
      ...mapActions([
        'updateContainerList', 'updateVMList'
      ])
    }
  }
</script>

<style scoped>

</style>
