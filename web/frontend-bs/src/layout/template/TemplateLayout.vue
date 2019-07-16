<template>
  <Layout
    :title="title"
    :logo="logo"
    :sidebar-background="sidebarBackground"
    :sidebar-color="sidebarColor"
    :sidebar-items="sidebarItems"></Layout>
</template>

<style lang="scss">
</style>

<script>
  import Layout from '../Layout.vue'

  export default {
    components: {
      Layout
    },
    data() {
      return {
        title: 'Template',
        logo: 'img/template-logo.png', //public/img/template-logo.png
        sidebarColor: 'black', //accepted: '', 'blue', 'azure', 'green', 'orange', 'red', 'purple', 'black';
        sidebarBackground: 'img/sidebar-5.jpg', //'' for solid background
        sidebarItems: [
          {
            to: '/admin/overview',
            icon: 'nc-icon nc-chart-pie-35',
            text: 'Dashboard'
          },
          {
            to: '/admin/user',
            icon: 'nc-icon nc-circle-09',
            text: 'User Profile'
          },
          {
            to: '/admin/table-list',
            icon: 'nc-icon nc-notes',
            text: 'Table List'
          },
          {
            to: '/admin/typography',
            icon: 'nc-icon nc-paper-2',
            text: 'Typography'
          },
          {
            to: '/admin/icons',
            icon: 'nc-icon nc-atom',
            text: 'Icons'
          },
          {
            to: '/admin/maps',
            icon: 'nc-icon nc-pin-3',
            text: 'Maps'
          },
          {
            to: '/admin/notifications',
            icon: 'nc-icon nc-bell-55',
            text: 'Notifications'
          },
        ]
      }
    }
  }

</script>
