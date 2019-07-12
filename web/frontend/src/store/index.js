import Vue from 'vue';
import Vuex from 'vuex';
import docker from './modules/docker';
import data from './modules/data';
import vms from './modules/vms';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    docker,
    data,
    vms
  }
});
