<template>
<div class="dockerhome">

    <div class="content">
        <div class="header">
            <strong>Home</strong>
            <font-awesome-icon :icon="['fas', 'home']" size="lg" pull="left" color="black" />
        </div>
        <br>
        <div class="info">
            <font-awesome-icon :icon="['fab', 'docker']" size="lg" color="rgb(111,111,111)" />
            <strong>Data collected 1</strong>
            <span class="badge badge-success">show running here</span>
            <hr>
            <table>
                <tr>
                    <td width="20px"></td>

                    <td width="200px">
                        <font-awesome-icon :icon="['fas', 'info-circle']" size="sm" color="rgb(111,111,111)" />
                        <strong> Header: </strong>
                    </td>
                    <td width="200px">
                        <font-awesome-icon :icon="['fas', 'info-circle']" size="sm" color="rgb(111,111,111)" />

                    </td>

                </tr>
            </table>
        </div>
    </div>
</div>
</template>

<script>
import DSidebar from '@@/components/DSidebar.vue'
import NavBar from '@@/component/Navbar.vue'

@Component({
    components: {
        DSidebar,
        NavBar
    }
})

export default {
    name: "DataHome"
    data () {
        return {
            network_devices: [],
            linux_bridges: [],
            nd_string: '',
            lb_string: ''
        }
    }
    mounted() {
        this.axios.get("/api/docker/network_devices").then(response => {
            var res = JSON.parse(response.data.result)['return']
        })
    }
}
</script>

<style scoped>

</style>