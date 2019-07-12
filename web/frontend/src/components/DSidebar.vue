<template lang="html">
    <div>
    <div class="dsidebar">

        <font-awesome-icon :icon="['fab', 'docker']" size=5x color='white'/><br><br>

        <router-link to="/docker/dockerdashboard">
            <button class="sidebar-item">
                <strong>Dashboard</strong><font-awesome-icon :icon="['fas', 'tachometer-alt']" size=lg pull='right' color="white"/>
            </button>
        </router-link>

        <router-link to="/docker/dockercontainer">
            <button class="sidebar-item">
                <strong>Container</strong><font-awesome-icon :icon="['fas', 'database']" size=lg pull='right' color="white"/>
            </button>
        </router-link>

        <router-link to="/docker/dockerimage">
            <button class="sidebar-item">
                <strong>Image</strong><font-awesome-icon :icon="['fas', 'clone']" size=lg pull='right' color="white"/>
            </button>
        </router-link>
        <router-link to="/docker/network">
            <button class="sidebar-item">
                <strong>Network</strong><font-awesome-icon :icon="['fas', 'network-wired']" size=lg pull='right' color="white"/>
            </button>
        </router-link>

        <router-link to="/docker/volume">
            <button class="sidebar-item">
                <strong>Volume</strong><font-awesome-icon :icon="['fas', 'boxes']" size=lg pull='right' color="white"/>
            </button>
        </router-link>

        <router-link to="/docker/swarm">
            <button class="sidebar-item">
                <strong>Swarm</strong><font-awesome-icon :icon="['fas', 'users']" size=lg pull='right' color="white"/>
            </button>
        </router-link>
        <router-link to="/docker/event">
            <button class="sidebar-item">
                <strong>Event</strong><font-awesome-icon :icon="['fas', 'history']" size=lg pull='right' color="white"/>
            </button>
        </router-link>

        <router-link to="/docker/host">
            <button class="sidebar-item">
                <strong>Host</strong><font-awesome-icon :icon="['fas', 'hdd']" size=lg pull='right' color="white"/>
            </button>
        </router-link>

        <router-link to="/docker/user">
            <button class="sidebar-item">
                <strong>User</strong><font-awesome-icon :icon="['fa', 'laptop-code']" size=lg pull='right' color="white"/>
            </button>
        </router-link>

        <router-link to="/docker/setting">
            <button class="sidebar-item">
                <strong>Setting</strong><font-awesome-icon :icon="['fas', 'cogs']" size=lg pull='right' color="white"/>
            </button>
        </router-link>
    </div>
    <!-- <router-view></router-view> -->
</div>
</template>

<script>
export default {
    methods: {

    }
}
</script>

<style lang="css" scoped>
.dsidebar{
    padding-top: 30px;
    float: left;
    /* border-radius: 20px; */
    width: 200px;
    height: 880px;
    background: rgb(62, 62, 62);
}

.sidebar-item{
    opacity: 0.7;
    width: 200px;
    border: none;
    text-align: left;
    background: rgb(62, 62, 62);
    padding: 5px 20px 5px 20px;
}
.sidebar-item:hover{
    opacity: 1;
    border-left: 4px solid rgb(255, 153, 0);
    background: rgb(35, 35, 35);
    box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
strong{
    color: white;
}

</style>
