<template>
  <card>
    <div class="info">
      <!--      <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />-->
      <strong>{{name}}</strong>
      <!--todo: align badge to the right-->
      <hr>
      <table>
        <tr>
          <td width='30px'></td>
          <td width='100px'>
            <font-awesome-icon :icon="['fas', 'info-circle']" size=lg color='rgb(111, 111, 111)' />
            <strong> Info: </strong>
          </td>
          <td width='120px'>
            <font-awesome-icon :icon="['fas', 'fire']" size=sm color='rgb(111, 111, 111)' />
            Class: {{functionClass}}
          </td>
          <td width='250px'>
            <font-awesome-icon :icon="['fas', 'file']" size=sm color='rgb(111, 111, 111)' />
            Size: {{filesize}}
            <!--            todo: add tooltips on hover-->
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
            <strong> OS: </strong>
          </td>
          <td width='250px'>
            {{os}}
          </td>
          <!--          todo: consider removing host cpu/os (customer knows nothing about docker so doesn't know containers run on host os or even that containers exist)-->
        </tr>
        <tr>
          <td width='30px'></td>
          <td width='130px'>
            <font-awesome-icon :icon="['fas', 'compass']" size=lg color='rgb(111, 111, 111)' />
            <strong> Description: </strong>
          </td>
          <td width='250px'>
            {{description}}
          </td>
        </tr>
      </table>
    </div>
  </card>
</template>

<script>
    export default {
        name: "VMImage",
      data () {
          return {
            name: 'Vyatta',
            functionClass: 'Router',
            filesize: '4 GB',
            os: 'Vyatta OS',
            description: "A very nice image"
          }
      }
    }
</script>

<style scoped>

</style>
