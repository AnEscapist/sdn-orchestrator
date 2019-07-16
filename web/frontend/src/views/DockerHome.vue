<template>
<div class="dockerhome">

    <div class="content">
        <div class='header'>
            <strong>Home</strong>
            <font-awesome-icon :icon="['fas', 'home']" size=lg pull='left' color="black" />
        </div>
        <br>

        <router-link to="/docker/dockerdashboard">
            
            <div class='info'>
                <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />
                <strong>Docker on uCPE ({{client['Name']}}) </strong>
                <span class="badge badge-success">Running</span>
                <hr>
                <table>
                    <tr>
                        <td width='30px'></td>
                        <td width='100px'>
                            <font-awesome-icon :icon="['fas', 'info-circle']" size=lg color='rgb(111, 111, 111)' />
                            <strong> Info: </strong>
                        </td>
                        <td width='250px'>
                            <font-awesome-icon :icon="['fas', 'database']" size=sm color='rgb(111, 111, 111)' />
                            {{client['Containers']}} containers -
                            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(81, 164, 81)' />
                            {{client['ContainersRunning']}}
                            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(237, 187, 66)' />
                            {{client['ContainersPaused']}}
                            <font-awesome-icon :icon="['fas', 'heartbeat']" size=sm color='rgb(204, 68, 74)' />
                            {{client['ContainersStopped']}}
                        </td>
                        <td width='120px'>
                            <font-awesome-icon :icon="['fas', 'clone']" size=sm color='rgb(111, 111, 111)' />
                            {{client['Images']}} images
                        </td>
                        <td>
                            <font-awesome-icon :icon="['fas', 'microchip']" size=sm color='rgb(111, 111, 111)' />
                            {{client['NCPU']}} CPU
                        </td>
                    </tr>
                    <tr>
                        <td width='30px'></td>
                        <td width='100px'>
                            <font-awesome-icon :icon="['fab', 'linux']" size=lg color='rgb(111, 111, 111)' />
                            <strong> OS: </strong>
                        </td>
                        <td width='250px'>
                            {{client['OperatingSystem']}}
                        </td>

                    </tr>


                </table>

            </div>
        </router-link>
        <br>
        <div class='info'>
            <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />
            <strong>Docker on uCPE (IP address) </strong>
            <span class="badge badge-danger">Exited</span>
            <hr>

        </div>
        <br>
        <div class='info'>
            <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />
            <strong>Docker on uCPE (IP address) </strong>
            <span class="badge badge-warning">Paused</span>
            <hr>

        </div>
    </div>

</div>
</template>

<script lang="ts">
import {
    Component,
    Vue
} from 'vue-property-decorator';
import DSidebar from '@/components/DSidebar.vue';
import NavBar from '@/components/NavBar';

@Component({
    components: {
        DSidebar,
        NavBar
    },
})
export default class DockerHome extends Vue {
    name: 'dockerhome'
    data() {
        return {
            containers: [],
            images: [],
            client: ''
        };
    }
    mounted() {
        this.axios.get("/api/docker/list_containers").then(response => {
            var res = JSON.parse(response.data.result)['return']
            var containers = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
            this.containers = containers
        });
        this.axios.get("/api/docker/list_images").then(response => {
            var res = JSON.parse(response.data.result)['return']
            var images = res.substring(res.indexOf('[') + 1, res.indexOf(']')).split(',')
            this.images = images
        });
        this.axios.get("/api/docker/client_info").then(response => {
            var res = JSON.parse(response.data.result)
            var client = JSON.parse(res['return'])
            this.client = client
        });
    }
    methods() {

    }
}
</script>

<style lang="css" scoped>
.header{
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(226, 226, 226);
    text-align: left;

}

.content{
    border: 1px, solid rgb(0, 0, 0);
    height: auto;
    margin-left: 220px;
    margin-right: 20px;
}
.info{
    font-size: 15px;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(240, 240, 240);
    text-align: left;

}

.ucpe{
    font-size: 15px;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(240, 240, 240);
    text-align: left;

}

.ucpe-info{
    width: 100px;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    background: rgb(226, 226, 226);
    text-align: left;

}


</style>
