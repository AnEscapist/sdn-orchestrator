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
  import templateSidebar from './templateSidebar'

  export default {
    components: {
      Layout
    },
    data() {
      return {
        title: 'template',
        home: '/admin/overview',
        logo: 'img/template-logo.png', //public/img/template-logo.png
        sidebar: templateSidebar
      }
    }
  }

</script>
