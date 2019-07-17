<template>
  <div class="wrapper">
    <div class="main-panel">
      <Sidebar
               :logo="logo"
               :title="title"
               :home="home"
               :image="sidebarBackgroundImage"
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
  import TopNavbar from '../components/layout/TopNavbar.vue'
  import ContentFooter from '../components/layout/ContentFooter.vue'
  import DashboardContent from '../components/layout/Content.vue'
  import MobileMenu from '../components/layout/MobileMenu.vue'
  import Sidebar from '../components/layout/sidebar/Sidebar.vue'
  export default {
    props: ['title', 'home', 'logo', 'sidebarColor', 'sidebarBackgroundImage', 'sidebarItems'],
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
