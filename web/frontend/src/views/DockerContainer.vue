<template>
<div class="dockercontainer">
    <div id="nav">
        <!-- <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> | -->

        <router-link to="/login">Login</router-link> |
        <router-link to="/docker">Docker</router-link>
        <DSidebar></DSidebar>

    </div>

    <div class="content">
        <div class='header'>
            <strong>Container</strong>
            <font-awesome-icon :icon="['fas', 'database']" size=lg pull='left' color="black" />
        </div>
        <br>

        <div class="action">
            <button type="button" class="btn btn-success"><font-awesome-icon :icon="['fas', 'play']" size=sm /> Start</button>
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

@Component({
    components: {
        DSidebar,
    },
})
export default class DockerContainer extends Vue {
    name: 'dashboard'
    data() {
        return {
            endpoint: '',
            content: ''
        };
    }
    mounted() {
        this.axios.get("../manifest.json").then(response => {
            console.log(response.data)
            this.endpoint = response.data.name
        });
        this.axios.post("http://api.komavideo.com/news/list").then(body => {
            this.content = body.data[0].title;
        })
    }
}
</script>

<style lang="css" scoped>

.header{
    background: red;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(226, 226, 226);
    text-align: left;

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
.content{
    border: 1px, solid rgb(0, 0, 0);
    height: auto;
    margin-left: 220px;
    margin-right: 20px;
}


</style>
