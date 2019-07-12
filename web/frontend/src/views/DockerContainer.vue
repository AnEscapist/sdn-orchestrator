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
            <div class="buttons">
                <button type="button" class="btn btn-success"><font-awesome-icon :icon="['fas', 'play']" size=sm /> Start</button>
                <button type="button" class="btn btn-danger"><font-awesome-icon :icon="['fas', 'square']" size=sm /> Stop</button>
                <button type="button" class="btn btn-danger"><font-awesome-icon :icon="['fas', 'skull-crossbones']" size=sm />  Kill</button>
                <button type="button" class="btn btn-primary"><font-awesome-icon :icon="['fas', 'sync-alt']" size=sm /> Restart</button>
                <button type="button" class="btn btn-primary"><font-awesome-icon :icon="['fas', 'pause']" size=sm /> Pause</button>
                <button type="button" class="btn btn-danger"><font-awesome-icon :icon="['fas', 'trash-alt']" size=sm /> Remove</button>
            </div>
            <div class="list">

            </div>

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

        };
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
.action{
    padding-top: 10px;
    padding-bottom: 5px;
    background: rgb(240, 240, 240);
}
button{
    font-size: 15px;
    width: 100px;
    margin-right: 2px;
}
.buttons{
}


</style>
