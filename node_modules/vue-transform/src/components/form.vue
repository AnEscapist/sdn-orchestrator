<script type="text/babel">
  import T from 'libt'
  import validate from '../json/validate.json'
  import icon from 'vue-awesome'
  import item from './item.vue'

  module.exports = {
    components: {
      icon: icon,
      item: item
    },
    props: {
      model: {
        type: Object,
        default: function () {
          return {}
        }
      },
      fields: {
        type: [Array, Object]
      },
      submit: {
        type: Function
      },
      onChange: {
        type: Function
      },
      onClose: {
        type: Function
      },
      size: {
        type: String,
        default: 'md',
        validator: T.contains(validate.Size)
      },
      icon: {
        type: String,
        default: ''
      },
      label: {
        type: String,
        default: ''
      },
      alert: {
        type: String,
        default: 'danger',
        validator: T.contains(validate.Alert)
      },
      text: {
        type: String,
        default: ''
      },
      buttons: {
        type: Array,
        default: function () {
          return []
        }
      }
    },
    data: function () {
      return {
        backup: T.copy(this.model),
        compact: !this.submit && !this.onChange,
        Fields: [],
        compile: [],
        objMode: false
      }
    },
    mounted: function () {
      this.load()
    },
    watch: {
      model: {
        deep: true,
        handler: function () {
          if (typeof this.onChange === 'function') {
            var diff = false
            Object.keys(this.model).forEach(key => {
              if (this.model[key] != this.$data.backup[key]) {
                diff = true
              }
            })
            if (diff && this.validateModel()) {
              this.$data.backup = T.copy(this.model)
              this.onChange(this.model)
            }
          }
        }
      },
      fields: function () {
        this.load()
      }
    },
    methods: {
      run: function () {
        if (this.$data.objMode) {
          var model = T.copy(this.model)
          this.$data.compile.forEach(key => {
            if (model[key] !== '') {
              try {
                eval(`model[key] = ${model[key]}`)
              } catch (err) {
                T.debug('Eval error', key, model[key], err.toString())
                model[key] = undefined
              }
            } else {
              model[key] = undefined
            }
          })

          this.$data.Fields.forEach(field => {
            if (field.format === 'boolean' && model[field.id] !== undefined) {
              model[field.id] = model[field.id] ? true : false
            } 
          })
          this.submit(model)
        } else if (typeof this.submit === 'function' && this.validateModel()) {
          this.submit(this.model)
          if (this.onClose) {
            this.onClose()
          }
        }
      },
      load: function () {
        T.sync(this.$data.compile, [])
        this.$data.objMode = false

        if (this.fields == null) {
          T.sync(this.$data.Fields, T.setFields(this.model))
        } else if (this.fields instanceof Array) {
          T.sync(this.$data.Fields, this.fields)
        } else {
          this.$data.objMode = true
          var fields = [
            {
              id: 'style',
              format: 'string'
            }, {
              id: 'class',
              format: 'string'
            }
          ]
          var model = {}
          
          this.$data.compile = []
          Object.keys(this.fields).forEach(key => {
            var prop = this.fields[key]
            if (prop.default !== undefined) {
              if (typeof prop.default === 'function' && prop.type !== Function) {
                model[key] = prop.default()
              } else {
                model[key] = prop.default
              }
            }

            if (prop.type instanceof Array) {
              var type = this.getType(prop.type[0])
            } else {
              var type = this.getType(prop.type)
            }

            var format = 'string'
            if (type === 'Boolean') {
              format = 'boolean'
            } else if (type === 'Number') {
              format = 'number'
            } else if (type === 'Array' || type === 'Object' || type === 'Function') {
              format = 'string:text'
              this.$data.compile.push(key)
            }

            fields.push({
              id: key,
              label: `${key} (${type})`,
              format: format,
              options: this.getOptions(prop.validator),
              required: prop.required
            })
          })

          model = T.merge(model)(this.model)
          var F = []
          model = T.iterate(value => {
            if (typeof value === 'function') {
              F.push(String(value))
              return `&&F:${F.length - 1}`
            } else {
              return value
            }
          })(model)
          Object.keys(model).forEach(key => {
            if (typeof model[key] === 'object' && model[key] != null) {
              model[key] = JSON.stringify(model[key], undefined, 2)
              F.forEach((f, i) => {
                model[key] = T.replaceAll(`"&&F:${i}"`, f)(model[key])
              })
            } else if (typeof model[key] === 'string' && model[key].substr(0, 4) === `&&F:`) {
              F.forEach((f, i) => {
                model[key] = model[key] === `&&F:${i}` ? f : model[key]
              })
            }
          })

          T.sync(this.model, model, this.$set)
          T.sync(this.$data.Fields, fields)
          this.run()
        }

        this.$data.Fields.forEach(field => {
          this.$set(this.model, field.id, T.parse(field.format)(this.model[field.id]))
        })
      },
      getOptions: function (validator) {
        if (validator) {
          var options = validator(T.identity)
          if (options instanceof Array) {
            return options
          }
        }
      },
      getType: function (type) {
        var ret = ''
        if (type === String) {
          ret = 'String'
        } else if (type === Number) {
          ret = 'Number'
        } else if (type === Boolean) {
          ret = 'Boolean'
        } else if (type === Object) {
          ret = 'Object'
        } else if (type === Array) {
          ret = 'Array'
        } else if (type === Function) {
          ret = 'Function'
        } else {
          ret = 'Object'
        }

        return ret
      },
      getClass: function () {
        if (['success', 'info', 'warning', 'danger'].indexOf(this.alert) !== -1) {
          return 'alert alert-' + this.alert
        } else {
          return 'well'
        }
      },
      validateModel: function () {
        var valid = true

        this.fields.forEach((field, i) => {
          field.format = field.format || 'string'
          if (field.format.indexOf(':file') === -1) {
            this.$set(this.model, field.id, T.parse(field.format)(this.model[field.id]))
          }
          this.$set(this.fields[i], 'error', '')
          var error = false
          var empty = this.model[field.id] == null
          var label = field.label || field.placeholder || field.id
          if (field.static) {
            return
          }
          if (field.format === 'json' && this.model[field.id]) {
            try {
              var x = JSON.parse(this.model[field.id])
            } catch (err) {
              this.$set(this.fields[i], 'error', `${label} ${err.toString()}`)
              valid = false
              error = true
            }
          }
          if (!error && empty && field.required) {
            if (field.format.substr(0, 6) === 'string' && !field.options && !field.src) {
              this.$set(this.model, field.id, '')
            }
          }
          if (!error && field.validate instanceof Array) {
            field.validate.forEach(v => {
              if (!error && !T.evaluate(v.assert)(this.model)) {
                this.$set(this.fields[i], 'error', `${label} ${v.error}`)
                valid = false
                error = true
              }
            })
          }
          if (!error && field.watchlen && (String(this.model[field.id]).length < field.watchlen || empty)) {
            valid = false
          }
        })

        return valid
      }
    }
  }
</script>

<template>
  <div class="thumbnail">
    <div v-if="onClose || label || icon" class="modal-header">
      <button v-if="onClose" type="button" class="close" @click="onClose">
        <icon name="times" class="glyphicon" />
      </button>
      <h4 v-if="label || icon" style="text-align:center" class="modal-title">
        <icon v-if="icon" :name="icon" class="glyphicon" /> {{label}}
      </h4>
    </div>
    <div v-if="Fields.length || text" class="modal-body">
      <div style="clear: both;"></div>
      <form class="form-horizontal" @submit.prevent="submit">
        <item
          v-for="(field, index) in Fields"
          :key="index"
          :model="model"
          v-bind="field"
          :static="field.static || compact"
          :compact="compact"
          :size="field.size || size"
        >
        </item>
      </form>
      <div style="clear: both;"></div>
      <div 
        v-if="text"
        :class="getClass()" 
        style="white-space:pre-wrap;"
      ><big>{{text}}</big></div>
      <div style="clear: both;"></div>
    </div>
    <div v-if="buttons.length" class="modal-footer">
      <button
        v-for="b in buttons"
        :class="[
          'btn',
          'btn-' + b.type,
          b.block ? 'btn-block' : '',
          b.size ? 'btn-' + b.size : 'btn-' + size
        ]"
        @click="b.click ? b.click(model) : run()"
      >
        <icon v-if="b.icon" :name="b.icon" class="glyphicon" />
        {{b.label}}
      </button>
    </div>
  </div>
</template>
