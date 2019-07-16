<template lang="html">
  <div class="docker">
      <div id="nav">
        <!-- <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> | -->

        <!-- <router-link to="/login">Login</router-link> |
        <router-link to="/docker">Docker</router-link>
        <DSidebar></DSidebar> -->
        <DSidebar></DSidebar>
        <NavBar></NavBar>
        <router-view></router-view>
      </div>


  </div>


</template>

<script>
import DSidebar from '@/components/DSidebar.vue';
import NavBar from '@/components/NavBar.vue'

export default {
    name: 'docker',
    data() {
        return {}
    },
    methods: {

    },
    components: {
        DSidebar,
        NavBar
    }
}
</script>

<style lang="scss">
#nav {
  padding: 10px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: rgb(255, 255, 255);
    }
  }
}
.docker{
    height: 948px;
}
</style>
