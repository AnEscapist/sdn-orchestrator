<template>
<div class="dockerhome">

    <div class="content">
        <div class='header'>
            <strong>Home</strong>
            <font-awesome-icon :icon="['fas', 'home']" size=lg pull='left' color="black" />
        </div>
        <br>
        <div class='info'>
            <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />
            <strong>Docker on uCPE (IP address) </strong>
            <span class="badge badge-success">Running</span>
            <hr>
            <table>
                <tr>
                    <td width='30px'></td>
                    <td width='200px'>
                        <font-awesome-icon :icon="['fas', 'info-circle']" size=sm color='rgb(111, 111, 111)' flip='horizontal' />
                        <strong> Info: </strong>
                    </td>


                    <td width='60px'>
                        <font-awesome-icon :icon="['fas', 'database']" size=sm color='rgb(111, 111, 111)' flip='horizontal' />
                        {{containers.length}}
                    </td>
                    <td>
                        <font-awesome-icon :icon="['fas', 'clone']" size=sm color='rgb(111, 111, 111)' flip='horizontal' />
                        {{images.length}}
                    </td>
                </tr>
                <tr>
                    <td width='30px'></td>
                    <td width='200px'>
                        <font-awesome-icon :icon="['fas', 'info-circle']" size=sm color='rgb(111, 111, 111)' flip='horizontal' />
                        <strong> Client: {{client}}</strong>
                    </td>



                </tr>
            </table>

        </div>
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
            client: 'x'
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
            console.log(response.data.result)
            var res = JSON.parse(response.data.result)
            var client = res
            this.client = client
        });
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
