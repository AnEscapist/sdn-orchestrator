import Vue from 'vue';
import Vuex from 'vuex';
import hostData  from './modules/hostData';
import vnfs from './modules/vnfs';
import login from './modules/login';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    hostData,
    vnfs,
    login
  }
});
