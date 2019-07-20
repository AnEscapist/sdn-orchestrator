<template>
<div class="content">
  <div class="container-fluid">
    <font-awesome-icon :icon="['fas', 'cogs']" size=lg color='rgb(0, 0, 0)' /> <strong> Actions</strong>
    <hr>
    <button type="button" class="btn btn-success btn-sm">
        <font-awesome-icon :icon="['fas', 'play']" size=lg color='green' />
        Start
    </button>
    <button type="button" class="btn btn-danger btn-sm">
        <font-awesome-icon :icon="['fas', 'square']" size=lg color='red' />
        Start
    </button>

  </div>
</div>
<!-- <div height='100%'>

    <div id='action'>
        <font-awesome-icon :icon="['fas', 'cogs']" size=lg color='rgb(0, 0, 0)' /> <strong> Actions</strong>
        <hr>

    </div>
</div> -->
</template>

<script>
import Card from '@/components/Cards/Card.vue'
export default {
  name: "DockerContainer",
  data: function() {
    return {}


  },
  created() {
    this.name = this.$route.query.name
  },
  mounted() {},
  methods: {

  }

}
</script>

<style scoped>
.container-fluid {
  border: 1px solid rgb(208, 208, 208);
  padding-top: 10px;
}
</style>
