<template lang="html">
  <div class="docker">
      <div id="nav">
        <!-- <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> | -->

        <router-link to="/login">Login</router-link> |
        <router-link to="/docker">Docker</router-link>

      </div>
      <DSidebar></DSidebar>
      <router-view></router-view>
  </div>


</template>

<script>
import DSidebar from '@/components/DSidebar.vue'

export default {
    name: 'docker',
    data() {
        return {}
    },
    methods: {

    },
    components: {
        DSidebar
    }
}
</script>

<style lang="scss" scoped>

</style>
