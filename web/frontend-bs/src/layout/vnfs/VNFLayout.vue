<template>
  <Layout
    :title="title"
    :home="home"
    :logo="logo"
    :sidebar-background-image="sidebar.backgroundImage"
    :sidebar-color="sidebar.color"
    :sidebar-items="sidebar.items"></Layout>
</template>

<style lang="scss">
</style>

<script>
  import Layout from '../Layout.vue'
  import vnfSidebar from './vnfSidebar'

  export default {
    components: {
      Layout
    },
    data() {
      return {
        title: 'virtual network functions',
        home: '/vnfs/dashboard',
        logo: 'img/router.png', //public/img/sample-pages-logo.png
        sidebar: vnfSidebar
      }
    }
  }

</script>
