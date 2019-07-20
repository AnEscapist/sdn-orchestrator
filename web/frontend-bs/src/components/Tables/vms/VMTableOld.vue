<template>
  <LTable class="table-hover"
          :columns="vmTableColumns"
          :data="Object.values(vmInfo)">
  </LTable>
</template>

<script>
  import { mapGetters } from 'vuex'
  import LTable from '../../Table'

  export default {
    name: "VMTableOld",
    components: {
      LTable
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
