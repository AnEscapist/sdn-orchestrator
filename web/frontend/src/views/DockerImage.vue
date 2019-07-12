<template>
<div class="dockerimage">
    <div id="nav">
        <!-- <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link> | -->

        <router-link to="/login">Login</router-link> |
        <router-link to="/docker">Docker</router-link>
        <DSidebar></DSidebar>

    </div>

    <div class="content">
        <div class='header'>
            <strong>Image</strong>
            <font-awesome-icon :icon="['fas', 'clone']" size=lg pull='left' color="black" />
        </div>

        <div class="pullimage">
            <font-awesome-icon :icon="['fas', 'download']" size=lg pull='left' color='rgb(117, 117, 117)' />
            <strong>Pull image</strong>
            <hr>
            <div class="pull-choice">

                <table>
                    <tr>
                        <td>
                            <form class="form-inline">
                                <strong style="font-size:20px">Image: &nbsp</strong>

                                <input type="text" class="form-control mb-2 mr-sm-2" id="inlineFormInputName2" placeholder="image name">

                                <div class="input-group mb-2 mr-sm-2">
                                    <div class="input-group-prepend">
                                        <div class="input-group-text">:</div>
                                    </div>
                                    <input type="text" class="form-control" id="inlineFormInputGroupUsername2" placeholder="image tag">
                                </div>

                            </form>
                        </td>

                        <td>
                            <form class="form-inline">
                                <strong style="font-size:20px">Repository: &nbsp</strong>
                                <input type="text" class="form-control mb-2 mr-sm-2" id="inlineFormInputName2" placeholder="docker hub">
                            </form>
                        </td>
                    </tr>
                </table>
                <br>
                <p class="note">
                    <font-awesome-icon :icon="['fas', 'exclamation-triangle']" size=sm />
                    Note: if you don't specify the tag of the image,  <span class="badge badge-pill badge-info">latest</span> will be used.</p>
            </div>
            <button type="button" class="btn btn-primary">
                <font-awesome-icon :icon="['fas', 'cloud-download-alt']" size=lg />
                Pull the image</button>



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
.pullimage{
    font-size: 15px;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    border: 1px solid rgb(180, 180, 180);
    background: rgb(240, 240, 240);
    text-align: left;

}
.pull-choice{
    margin-left: 8px;
}
.note{
    color: rgb(255, 158, 45);
}


</style>
