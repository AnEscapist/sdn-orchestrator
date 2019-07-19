<template>
  <div>
    <card>
      <h1>Roger's Playground</h1>
      <h2>VNF Count: {{vnfCount}}</h2>
      <h2>VNF List: {{vnfList}}</h2>
      <h2>VM List: {{vmList}}</h2>
      <h2>VM Info: {{vmInfo}}</h2>
      <LTable class="table-hover"
               :columns="vmTableColumns"
               :data="Object.values(vmInfo)">
      </LTable>
    </card>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import LTable from '../../components/Table.vue'

  export default {
    name: "RogerTest",
    components: {
      LTable
    },
    data() {
      return {
        vmTableColumns: ['Name', 'State', 'Memory Usage', 'Memory Allocated', 'CPUs', 'CPU Time']
      }
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
