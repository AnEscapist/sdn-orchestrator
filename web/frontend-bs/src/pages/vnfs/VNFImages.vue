<template>
  <div class="content">
    <div class="container-fluid">
      <VNFImageSummary/>
      <div v-for="imageData in Object.values(vmImageInfo)" :key="imageData.name">
      <VMImage :imageData="imageData"></VMImage>
      </div>
    </div>
  </div>
</template>

<script>
  import VNFImageSummary from '../../components/Cards/vnfs/VNFImageSummary'
  import VMImage from '../../components/Cards/vnfs/vms/VMImage'
  import {mapActions, mapGetters} from 'vuex'

  export default {
    name: "VNFImages",
    components: {
      VNFImageSummary, VMImage
    },
    computed: {
      ...mapGetters(['vmImageInfo'])
    },
    methods: {
      ...mapActions(['updateVMImageInfo'])
    },
    created () {
      console.log("created");
      this.updateVMImageInfo();
    }
  }
</script>

<style scoped>

</style>
