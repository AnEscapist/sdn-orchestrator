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
  import hostInfoSidebar from './hostInfoSidebar'

  export default {
    components: {
      Layout
    },
    data() {
      return {
        title: 'host info',
        home: '/host-data/overview',
        logo: 'img/icons/host-data.jpg', //public/img/sample-pages-logo.png
        sidebar: hostInfoSidebar
      }
    }
  }

</script>
