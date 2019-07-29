<template>
  <b-form inline>
    <label class='mr-sm-2'
    >VLAN Tag: eth{{interface}}</label>
    <b-input
      id="inline-form-input-name"
      class="col-md-3"
      placeholder="1-4095"
    ></b-input>
  </b-form>
</template>

<script>
    export default {
        name: "vmOVSVLANInput",
        props: ['interface']
    }
</script>

<style scoped>

</style>
