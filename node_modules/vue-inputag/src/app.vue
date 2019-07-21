<script type="text/babel">
  import Vue from '../node_modules/vue/dist/vue.js'
  import inputag from './index.vue'
  import VueGitHubCorners from 'vue-gh-corners'

  Vue.use(VueGitHubCorners)

  new Vue({
    components: {
      'vue-inputag': inputag
    },
    data: {
      model: {
        number: 3.14,
        integer: 25,
        date: '2018-01-01',
        string: 'Fork me on github',
        text: 'This is a sample text\nEdit as many times as you want',
        scientist: 'Gauss',
        country: 2,
        file: null,
        msg: 'hello world!',
        button: 'alert!'
      },
      click: (data) => {window.alert(data.msg)},
      github: 'https://github.com/marcodpt/vue-inputag',
      options: [
        "Eistein",
        "Newton",
        "Gauss",
        "Euler",
        "Riemann"
      ],
      options2: [
        {
          id: 1,
          label: 'Italy'
        }, {
          id: 2,
          label: 'France'
        }, {
          id: 3,
          label: 'Germany'
        }, {
          id: 4,
          label: 'England'
        }
      ]
    }
  }).$mount('#app')
</script>
