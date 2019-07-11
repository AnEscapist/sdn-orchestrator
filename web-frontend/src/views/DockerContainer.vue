<template>
  <div class="container">

  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import DSidebar from '@/components/DSidebar.vue'

@Component({
  components: {
      DSidebar,
  },
})
export default class Container extends Vue {}
</script>

<style lang="css" scoped>


</style>
