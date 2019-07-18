import Vue from 'vue';
import Vuex from 'vuex';
import hostData  from './modules/hostData';
import vnfs from './modules/products';
import login from './modules/login';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    product,
    cart,
    login
  }
});
