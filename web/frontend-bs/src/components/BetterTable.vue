<template>
  <div>
    <h1>I am a better table</h1>
  </div>
</template>
<script>
  export default {
    name: 'l-table',
    props: {
      columns: Array, //todo: rewrite this to take in an object mapping column name --> data object key
      data: Array
    },
    methods: {
      hasValue (item, column) {
        return item[column.toLowerCase()] !== 'undefined'
      },
      itemValue (item, column) {
        return item[column.toLowerCase()]
      }
    }
  }
</script>
<style>
</style>
