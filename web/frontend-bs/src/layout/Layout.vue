<template>
  <div class="wrapper">
    <div class="main-panel">
      <Sidebar
               :logo="logo"
               :title="title"
               :image="sidebarBackground"
               :color="sidebarColor"
               :items="sidebarItems"
      ></Sidebar>
      <top-navbar></top-navbar>
      <dashboard-content @click="toggleSidebar">
      </dashboard-content>
      <content-footer></content-footer>
    </div>
  </div>
</template>

<style lang="scss">
</style>

<script>
  import TopNavbar from './sublayouts/TopNavbar.vue'
  import ContentFooter from './sublayouts/ContentFooter.vue'
  import DashboardContent from './sublayouts/Content.vue'
  import MobileMenu from './sublayouts/MobileMenu.vue'
  import Sidebar from './sublayouts/sidebar/Sidebar.vue'
  export default {
    props: ['title', 'logo', 'sidebarColor', 'sidebarBackground', 'sidebarItems'],
    components: {
      Sidebar,
      TopNavbar,
      ContentFooter,
      DashboardContent,
      MobileMenu
    },
    methods: {
      toggleSidebar () {
        if (this.$sidebar.showSidebar) {
          this.$sidebar.displaySidebar(false)
        }
      }
    },
  }
</script>
