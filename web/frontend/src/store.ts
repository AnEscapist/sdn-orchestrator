import Vue from 'vue';
import Vuex from 'vuex';
import docker from './store/modules/';
import data from './store/modules/';
import vms from './store/modules/';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    docker,
    data,
    vms
  }
});

