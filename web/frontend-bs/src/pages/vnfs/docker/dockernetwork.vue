<template>
<div class="content">
  <div class="container-fluid">
      <h3>To be continued...</h3>


  </div>
  <hr>


</div>
</template>

<script>
import Card from '@/components/Cards/Card.vue'
export default {
  name: "DockerNetwork",
  inject: ['reload'],
  data: function() {
    return {

    }


  },
  created() {
    // this.short_id = this.$route.query.short_id

  },
  mounted() {


  },
  methods: {


  }

}
</script>

<style scoped>
.container-fluid {
  border: 1px solid rgb(208, 208, 208);
  padding-top: 15px;
  padding-bottom: 13px;
}

a {
  color: #1b7fbd;
}

font {
  font-weight: bold;
}

input {
  height: 18px;
  /* background-color: red; */
  background-color: rgb(247, 247, 247);
  border: none;
  border-bottom: 1px solid rgb(89, 89, 89);
  padding-left: 3px;
  margin-bottom: 0px;
}

.renameBtn {
  background-color: white;
  border: 0px solid black;
  padding: 0;
}

.renameBtn:active {
  outline: none;
  padding: 0;
}

.inner-pre {
  font-family: Arial, sans-serif;
  font-weight: bold;
  font-size: 12px;
}

#console {
  background-color: red;
}

#textR {
  text-align: right;
}

h6 {
  text-transform: none;
}

hr {
  padding-top: 0;
  margin-top: 0px;

}

.btn-group-xs>.btn,
.btn-xs {
  padding: .25rem .4rem;
  font-size: .875rem;
  line-height: .5;
  border-radius: .2rem;
}
</style>
