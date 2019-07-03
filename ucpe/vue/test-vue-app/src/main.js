import Vue from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io'

Vue.config.productionTip = false

Vue.use(new VueSocketIO({debug: true, connection:'http://10.10.81.200:5000'}))

new Vue({
  render: h => h(App),
}).$mount('#app')
