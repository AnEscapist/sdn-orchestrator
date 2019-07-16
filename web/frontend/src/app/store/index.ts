import Vue from 'vue';
import Vuex from 'vuex';
import data from './modules/data';
import docker from './modules/docker';
import vms from './modules/vms';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        data,
        docker,
        vms
    }
});
