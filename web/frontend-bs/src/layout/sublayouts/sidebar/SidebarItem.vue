<template>
  <sidebar-link :to="item.to">
    <i :class="item.icon"></i>
    <p>{{item.text}}</p>
  </sidebar-link>
</template>

<script>
    export default {
        name: "SidebarItem",
        props: ['item']
    }
</script>

<style scoped>

</style>
