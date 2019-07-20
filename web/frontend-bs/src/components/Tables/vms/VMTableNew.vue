<template>
  <TMX></TMX>
</template>

<script>
  import { mapGetters } from 'vuex'
  import TMX from '../../Table'

  export default {
    name: "VMTableNew",
    components: {
      TMX
    },
    data() {
      return {
        vmTableColumns: ['Name', 'State', 'Memory Usage', 'Memory Allocated', 'CPUs'] //todo: figure out how to implement running time
      }
    },
    computed: {
      ...mapGetters([
        'vnfList', 'vnfCount', 'vmList', 'vmInfo'
      ])
    },
  }
</script>

<style scoped>

</style>
