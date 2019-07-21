<script type="text/babel">
  import T from 'libt'
  import validate from '../json/validate.json'
  import inputag from 'vue-inputag'

  module.exports = {
    components: {
      'vue-inputag': inputag
    },
    props: {
      static: {
        type: Boolean,
        default: false
      },
      col: {
        type: Number,
        default: 1,
        validator: function (value) {
          return [0, 1, 2, 3, 4].indexOf(value) === value
        }
      },
      format: {
        type: String,
        default: 'string',
        validator: function (value) {
          value = value.split ? value.split(':')[0] : value
          return !value || T.contains(validate.Type)(value)
        }
      },
      label: {
        type: String
      },
      error: {
        type: String,
        default: ''
      },
      size: {
        type: String,
        default: 'md',
        validator: T.contains(validate.Size)
      },
      compact: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      getType: function () {
        var F = this.format.split(':')

        if (this.static) {
          return ''
        }

        if (this.$attrs.options || this.$attrs.source) {
          return 'select'
        } else if (F[0] === 'boolean') {
          return 'checkbox'
        } else if (F[0] === 'date') {
          return 'date'
        } else if (F[0] === 'json') {
          return 'textarea'
        } else if (F.indexOf('pass') !== -1) {
          return 'password'
        } else if (F.indexOf('file') !== -1) {
          return 'file'
        } else if (F.indexOf('color') !== -1) {
          return 'color'
        } else if (F.indexOf('text') !== -1) {
          return 'textarea'
        } else if (F.indexOf('pgb') !== -1) {
          return this.static ? 'progressbar' : 'range'
        } else {
          return 'text'
        }
      },
      getClass: function () {
        if (this.static) {
          return 'form-control-static'
        } else if (['select', 'checkbox'].indexOf(this.getType()) === -1) {
          return 'form-control input-' + this.size
        } else {
          return ''
        }
      }
    }
  }
</script>

<template>
  <div
    :class="[
      compact ? '' : 'form-group', 
      'form-group-' + size,
      error ? 'has-error': '', 
      col > 0 ? ('col-xs-' + Math.floor(12 / col)) : ''
    ]"
  >
    <label
      v-if="label !== '' && col"
      :class="['control-label', 'col-xs-' + (2 * col)]"
    >
      {{label || $attrs.id}}:
    </label>
    <div :class="[
      'col-xs-' + (12 - (label !== '' ? 2 * col : 0)),
      getType() === 'checkbox' ? 'checkbox' : ''
    ]">
      <vue-inputag
        v-if="!static"
        v-bind="$attrs"
        :class="getClass()"
        :type="getType()"
      />
      <p v-else class="form-control-static">
        <vue-inputag
          v-bind="$attrs"
          :type="getType()"
        />
      </p>
      <span class="help-block" v-if="error">
        {{error}}
      </span>
    </div>
  </div>
</template>
