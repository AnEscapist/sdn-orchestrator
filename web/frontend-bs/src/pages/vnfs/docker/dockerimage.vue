<template>
<div class="content">
  <div class="container-fluid">
    <font-awesome-icon :icon="['fas', 'clone']" size=lg color='rgb(0, 0, 0)' /> <strong> Image details - </strong>
    {{name}}
    <hr>
    <pre>{{image_info}}</pre>
  </div>
</div>
</template>

<script>
import Card from '@/components/Cards/Card.vue'
export default {
  name: "DockerImage",
  data: function() {
    return {
        image_info: ''
    }


  },
  created() {
    this.name = this.$route.query.name

  },
  mounted() {
    // this.axios.get("/api/docker/inspect_container", {
    //   params: {
    //     id_name: this.short_id
    //   }
    // }).then(response => {
    //   var inspect = JSON.parse(response.data.result)['return']
    //   this.inspect = inspect
    //   this.status = inspect['State']['Status']
    //   this.setBtn(this.status)
    //   this.ip = inspect['NetworkSettings'].IPAddress
    //   this.id = inspect['Id']
    //   this.name = inspect['Name'].slice(1, inspect['Name'].legth)
    //   this.createTime = inspect['Created']
    // });
    this.axios.get('/api/docker/images_info', {
        params: {
            name: this.name
        }
    }).then(response => {
        console.log(typeof(response.data.result))
        console.log(JSON.parse(response.data.result)['return'])
        var image_info = JSON.parse(response.data.result)['return']
        this.image_info = image_info
        console.log(typeof(this.image_info))
        // res = JSON.parse(image_info)

    })

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
</style>
