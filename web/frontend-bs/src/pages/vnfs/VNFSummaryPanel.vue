<template>
  <card>
    <div class="info">
<!--      <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />-->
      <strong>VNF Summary</strong>
      <span class="badge badge-success">Connected</span>
<!--todo: align badge to the right-->
      <hr>
      <table>
        <tr>
          <td width='30px'></td>
          <td width='100px'>
            <font-awesome-icon :icon="['fas', 'info-circle']" size=lg color='rgb(111, 111, 111)' />
            <strong> Info: </strong>
          </td>
          <td width='250px'>
            <font-awesome-icon :icon="['fas', 'database']" size=sm color='rgb(111, 111, 111)' />
            10 VNFs -
            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(81, 164, 81)' />
            6
            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(237, 187, 66)' />
            3
            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(204, 68, 74)' />
            1
<!--            todo: add tooltips on hover-->
          </td>
          <td width='120px'>
            <font-awesome-icon :icon="['fas', 'clone']" size=sm color='rgb(111, 111, 111)' />
            23 Images
          </td>
          <td>
            <font-awesome-icon :icon="['fas', 'microchip']" size=sm color='rgb(111, 111, 111)' />
            16 CPUs
          </td>
        </tr>
        <tr>
          <td width='30px'></td>
          <td width='100px'>
            <font-awesome-icon :icon="['fab', 'linux']" size=lg color='rgb(111, 111, 111)' />
            <strong> Host OS: </strong>
          </td>
          <td width='250px'>
            Ubuntu 18.04
          </td>
<!--          todo: consider removing host cpu/os (customer knows nothing about docker so doesn't know containers run on host os or even that containers exist)-->
        </tr>
      </table>
    </div>
  </card>
</template>

<script>
    export default {
        name: "VNFSummaryPanel",
        components:{

        }
    }
</script>

<style scoped>

</style>
