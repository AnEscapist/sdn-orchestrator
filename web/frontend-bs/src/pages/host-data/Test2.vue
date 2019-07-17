<template>
    <h1> This is a test. {{ mem }} blah </h1>
</template>

<script>
    export default {
        name: "Test2",
        data() {
          return {
            mem: ''
          }
        },
        mounted() {
          this.getMem()
        },
        methods: {
          getMem(){
            this.axios.get("/api/grpc/total_mem").then(response => {
              var res = JSON.parse(response.data.result)['return']
              this.mem = res
            });
          }
        }
    }
</script>

<style scoped>

</style>
