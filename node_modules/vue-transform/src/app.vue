<script type="text/babel">
  import T from 'libt'
  import Vue from '../node_modules/vue/dist/vue.js'
  import VueGitHubCorners from 'vue-gh-corners'
  import {modal, transform} from './index.vue'
  import form from './json/form.json'

  Vue.use(VueGitHubCorners)

  Vue.component('transform', transform)
  Vue.component('modal', modal)

  form.fields.forEach((field, i) => {
    if (field.source === '&country') {
      form.fields[i].source = function (model, callback) {
        callback(['Russia', 'Italy', 'Brazil'])
      }
    } else if (field.source === '&city') {
      form.fields[i].source = function (model, callback) {
        if (model.country === 'Russia') {
          callback([
            {id: 1, label: 'Moscow'},
            {id: 2, label: 'St. Petersburg'}
          ])
        } else if (model.country === 'Italy') {
          callback(['Roma', 'Veneza', 'Milao'])
        } else if (model.country === 'Brazil') {
          callback(['Sao Paulo', 'Rio de Janeiro', 'Porto Alegre', 'Manaus'])
        } else {
          callback(['Unknown'])
        }
      }
    } else if (field.source === '&banana') {
      form.fields[i].source = function (model, callback) {
        callback(['Apple', 'Banana'])
      }
    }
  })

  new Vue({
    data: function () {
      return {
        modal: null,
        tests: {
          label: 'Test Form',
          model: form.model,
          fields: form.fields,
          submit: function (model) {
            console.log('You submmitted me')
            console.log(model)
            console.log(model.file)
            setTimeout(() => {
              this.$set(this.$root.$data, 'modal', {
                label: 'Success',
                icon: 'check',
                text: 'You submmitted me\n' + JSON.stringify(model, undefined, 2),
                alert: 'success',
                buttons: [
                  {
                    type: 'danger',
                    label: 'Close',
                    icon: 'times',
                    click: 'hide'
                  }
                ]
              })
            }, 500)
          },
          buttons: [
            {
              type: 'primary',
              label: 'Submit',
              icon: 'check'
            }, {
              type: 'danger',
              label: 'Close',
              icon: 'times',
              click: 'hide'
            }
          ]
        },
        ready: false,
        form: null,
        model: null,
        fields: null,
        buttons: [
          {
            type: 'primary',
            icon: 'cog',
            label: 'Rebuild'
          }, {
            type: 'warning',
            label: 'Open Modal',
            icon: 'star',
            click: this.openModal
          }
        ]
      }
    },
    methods: {
      submit: function (data) {
        this.$data.form = T.copy(data)
        this.$data.ready = true
      },
      build: function () {
        this.$data.ready = false
        this.$data.model = T.copy(this.tests)
        this.$data.fields = T.copy(transform.props)
      },
      openModal: function (data) {
        this.$set(this.$root.$data, 'modal', this.$data.form)
      }
    },
    mounted: function () {
      this.build()
    }
  }).$mount('#app')
</script>
