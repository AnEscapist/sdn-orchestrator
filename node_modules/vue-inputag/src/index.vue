<script type="text/babel">
  import select from './select.vue'

  module.exports = {
    components: {
      'v-select': select
    },
    props: {
      model: {
        type: Object,
        required: true
      },
      id: {
        type: String,
        required: true
      },
      type: {
        type: String,
        default: 'text'
      },
      formatter: {
        type: Function,
        default: x => x
      },
      dependencies: {
        type: Array,
        default: () => []
      },
      click: {
        type: Function
      },
      href: {
        type: String,
        default: ''
      },
      options: {
        type: Array,
        default: () => []
      },
      source: {
        type: Function,
        default: function (model, callback) {
          callback(this.options)
        }
      },
      required: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      change: function (id, files) {
        this.model[this.id] = files
      },
      getStyle: function () {
        return {
          'white-space': String(this.model[this.id]).match(/\n/) ? 'pre-wrap' : null
        }
      },
      getBarColor: function () {
        var value = parseInt(this.model[this.id])
        value = isNaN(value) || value < 0 ? 0 : value
        value = value > 100 ? 100 : value

        return `hsl(${(100 - value) / 100 * 240}, 100%, ${value / 4 + 25}%)`
      },
      onClick: function () {
        if (this.click) {
          this.click(this.model)
        }
      },
      parseHref: function (href) {
        Object.keys(this.model).sort().reverse().forEach(key => {
          while (href.indexOf(`:${key}`) !== -1 && this.model[key] != null) {
            href = href.replace(`:${key}`, this.model[key])
          }
        })

        return href
      }
    }
  }
</script>

<template>
  <v-select
    v-if="type === 'select'"
    :model="model"
    :id="id"
    :dependencies="dependencies"
    :options="options"
    :source="source"
    :required="required"
    v-bind="$attrs"
  />
  <textarea
    v-else-if="type === 'textarea'"
    v-model="model[id]"
    :id="id"
  />
  <input 
    v-else-if="type === 'file'"
    type="file"
    :id="id"
    @change="change($event.target.name, $event.target.files)"
  />
  <div v-else-if="type === 'progressbar'" :style="{
      'min-width': '100px',
      'border-radius': '5px',
      'background-color': 'lightgrey'
    }"
  >
    <div
      :style="{
        'text-align': 'center',
        'width': (model[id] > 100 ? 100 : model[id]) + '%',
        'border-radius': '5px',
        'background-color': getBarColor(),
        'color': 'white',
        'overflow-x': 'hidden'
      }"
    >	
      {{model[id]}}%
    </div>
  </div>
  <input 
    v-else-if="type"
    :type="type"
    :id="id"
    v-model="model[id]"
  />
  <button v-else-if="click" @click="onClick"><slot></slot>{{formatter(model[id])}}</button>
  <a v-else-if="href"
    :href="parseHref(href)"
    :style="getStyle()"
    target="_blank"
  ><slot></slot>{{formatter(model[id])}}</a>
  <span v-else :style="getStyle()"><slot></slot>{{formatter(model[id])}}</span>
</template>
