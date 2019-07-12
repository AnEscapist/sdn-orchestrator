<template>
    <div id="nav">
        <!-- <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> | -->

        <router-link to="/login">Login</router-link> |
        <router-link to="/docker">Docker</router-link>
        <router-link to="/libvirt">Virtual Machines</router-link>
        <router-link to="/grpc">GRPC</router-link>
        <DSidebar></DSidebar>

    </div>
</template>

<script>
    import
    export default {
        name: "navbar"
    }
</script>

<style scoped>

</style>