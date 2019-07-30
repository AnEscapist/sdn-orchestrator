<template>
  <card>
    <div class="info">
      <!--      <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />-->
      <strong>VNF Image Summary</strong>
      <!--todo: align badge to the right-->
      <hr>
      <table>
        <tr>
          <td width='30px'></td>
          <td width='100px'>
            <font-awesome-icon :icon="['fas', 'info-circle']"
                               size=lg
                               color='rgb(111, 111, 111)'/>
            <strong> Info: </strong>
          </td>
          <td width='120px'>
            <font-awesome-icon :icon="['fas', 'clone']"
                               size=sm
                               color='rgb(111, 111, 111)'/>
            {{vmNumberImagesAvailable}} Images
          </td>
        </tr>
        <tr>
          <!--          todo: consider removing host cpu/os (customer knows nothing about docker so doesn't know containers run on host os or even that containers exist)-->
        </tr>
      </table>
    </div>
  </card>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'

  export default {
    name: "VNFImageSummary",
    computed: {
      ...mapGetters([
        'vmNumberImagesAvailable'
      ])
    },
  }
</script>

<style scoped>

</style>
