<template>
  <side-bar :title="title"
            :logo="logo"
            :background-color="color"
            :background-image="image"
  >
        <mobile-menu slot="content"></mobile-menu>
    <SidebarItem
      v-for="(item, i) in items"
      :key="i"
      :item="item"
    ></SidebarItem>
    <template slot="bottom-links">
      <sidebar-link class="active"
                    to="/admin/upgrade">
        <i class="nc-icon nc-alien-33"></i>
        <p>Upgrade to PRO</p>
      </sidebar-link>
    </template>
  </side-bar>
</template>

<script>
  import MobileMenu from '../MobileMenu'
  import SidebarItem from './SidebarItem.vue'

  export default {
    name: "Sidebar",
    props: ['logo', 'title', 'items', 'image', 'color'],
    components: { SidebarItem, MobileMenu },
  }
</script>

<style scoped>

</style>
