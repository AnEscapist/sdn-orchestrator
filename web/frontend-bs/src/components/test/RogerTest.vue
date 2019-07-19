<template>
    <div>
      <card>
      <h1>Roger's Playground</h1>
        <h2>VNF Count: {{vnfCount}}</h2>
        <h2>VNF List: {{vnfList}}</h2>
        <h2>VM List: {{vmList}}</h2>
        <h2>VM Info: {{vmInfo}}</h2>
      </card>
    </div>
</template>

<script>
  import {mapGetters, mapActions} from 'vuex'
    export default {
        name: "RogerTest",
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
