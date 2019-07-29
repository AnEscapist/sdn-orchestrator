<template>
  <div class="content">
    <div class="container-fluid">
      <VNFImageSummary/>
      <VMImage></VMImage>
    </div>
  </div>
</template>

<script>
  import VNFImageSummary from '../../components/Cards/vnfs/VNFImageSummary'
  import VMImage from '../../components/Cards/vnfs/vms/VMImage'

  export default {
    name: "VNFImages",
    components: {
      VNFImageSummary, VMImage
    }
  }
</script>

<style scoped>

</style>
