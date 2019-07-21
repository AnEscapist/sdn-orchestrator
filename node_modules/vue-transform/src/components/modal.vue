<script type="text/babel">
  import form from './form.vue'
  import overBody from 'vue-over-body'

  module.exports = {
    components: {
      'v-form': form,
      'vue-over-body': overBody
    },
    watch: {
      '$root.$data.modal': function () {
        this.open(this.$root.$data.modal)
      }
    },
    data: function () {
      return {
        index: 99999,
        isOpen: 0,
        size: 0
      }
    },
    methods: {
      hide: function () {
        this.$data.isOpen = 0
        this.$root.$data.modal = null
      },
      open: function (x) {
        if (x == null) {
          return
        }

        if ((x.fields || Object.keys(x.model || {})).length) {
          this.$data.size = 900 
        } else {
          this.$data.size = 300
        }

        if (x.buttons && x.buttons.forEach) {
          x.buttons.forEach(button => {
            if (button.click === 'hide') {
              button.click = this.hide
            }
          })
        }

        x.onClose = this.hide
        this.$data.isOpen = ++this.$data.index
      }
    }
  }
</script>

<template>
  <vue-over-body :open="isOpen" :dialog-style="{'width': size + 'px'}" before="before" after="after">
    <v-form v-bind="$root.$data.modal"/>
  </vue-over-body>
</template>

<style>
  .before {
    opacity: 0;
    top: -100px;
    max-width: 90%;
    margin: 30px auto;
  }
  .after {
    top: 0;
    opacity: 1;
  }
</style>
