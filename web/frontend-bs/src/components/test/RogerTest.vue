<template>
    <div>
      <card>
      <h1>Roger's Playground</h1>
        <h2>VNF Count: {{VNFCount}}</h2>
        <h2>VNF List: {{VNFList}}</h2>
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
        },
        computed: {
          ...mapGetters([
            'VNFList', 'VNFCount'
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
