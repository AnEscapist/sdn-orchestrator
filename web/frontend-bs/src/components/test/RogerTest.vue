<template>
    <div>
      <card>
      <h1>Roger's Playground</h1>
        <button @click="updateVNFList">Dispatch updateVNFList</button>
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
          this.$store.dispatch('updateVNFList')
        },
        computed: {
          ...mapGetters([
            'VNFList', 'VNFCount'
          ])
        },
        methods: {
          ...mapActions([
            'updateVNFList'
          ])
        }
    }
</script>

<style scoped>

</style>
