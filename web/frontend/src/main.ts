import Vue from 'vue';
import App from './App.vue';
import router from './router/router';
import store from './app/store';
import './registerServiceWorker';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'vuetify/dist/vuetify.min.css';
import "vue-material-design-icons/styles.css"
import axios from 'axios';
import VueAxios from 'vue-axios';
import Vuetify from 'vuetify';
import {library} from '@fortawesome/fontawesome-svg-core';
import {faUserSecret} from '@fortawesome/free-solid-svg-icons';
import {fas} from '@fortawesome/free-solid-svg-icons'
import {far} from '@fortawesome/free-regular-svg-icons'
import {fab} from '@fortawesome/free-brands-svg-icons'
import {FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText} from '@fortawesome/vue-fontawesome'

library.add(fas, far, fab, faUserSecret)

Vue.use(VueAxios, axios)
Vue.use(Vuetify, {iconfont: 'mdi'})
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.component('font-awesome-layers', FontAwesomeLayers)
Vue.component('font-awesome-layers-text', FontAwesomeLayersText)

Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: (h) => h(App),
}).$mount('#app');
