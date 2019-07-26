<template>
<div class="content">
  <div class="container-fluid">



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
      status: '',
      ip: '',
      id: '',
      name: '',
      createTime: '',
      inspect: '',
      stats: '',
      showIns: false,
      showEdit: true,
      showStats: false,
      newName: '',
      port_listening: 'no',
    }


  },
  created() {
    this.short_id = this.$route.query.short_id

  },
  mounted() {
    this.axios.get('/api/docker/check_port').then(response => {
      // console.log(typeof(response.data))
      this.port_listening = response.data
    })

    this.axios.get("/api/docker/inspect_container", {
      params: {
        id_name: this.short_id
      }
    }).then(response => {
      var inspect = JSON.parse(response.data.result)['return']
      this.inspect = inspect
      this.status = inspect['State']['Status']
      this.setBtn(this.status)
      this.ip = inspect['NetworkSettings'].IPAddress
      this.id = inspect['Id']
      this.name = inspect['Name'].slice(1, inspect['Name'].legth)
      this.createTime = inspect['Created']
    });

    this.axios.get('/api/docker/container_stats', {
      params: {
        id_name: this.short_id
      }
    }).then(response => {
      // console.log(response.data.result)
      var stats = JSON.parse(response.data.result)['return']
      this.stats = stats
    })

  },
  methods: {
    changeStatus(change_to) {
      this.axios.get('/api/docker/kill_port').then(response => {

        this.axios.get("/api/docker/change_status", {
          params: {
            id_name: this.short_id,
            change_to: change_to
          }
        }).then(response => {
          // console.log(response)
          var res = JSON.parse(response.data.result)['return']
          var status = res.substring(res.indexOf('[') + 1, res.indexOf(']'))

          this.update()

        });

      })


    },
    showInspect() {
      this.showStats = false;
      this.showIns = !this.showIns;
    },
    showStatistic() {
      this.showIns = false;
      this.showStats = !this.showStats
    },
    renameContainer(newName) {
      this.showEdit = !this.showEdit
      var tmp = this.name
      this.axios.get('/api/docker/rename_container', {
        params: {
          id_name: this.id,
          newName: newName
        }
      }).then(response => {
        var res = JSON.parse(response.data.result)['return']
        if (res) {
          this.name = JSON.parse(response.data.result)['return']
        } else {
          this.name = tmp
        }
      })
    },

    removeContainer() {
      this.axios.get('/api/docker/kill_port').then(response => {

        this.axios.get('/api/docker/remove_container', {
          params: {
            id_name: this.id,
          }
        }).then(response => {
            // console.log('container name', this.name)
            this.axios.get('/api/grpc/ovs_docker_del_port', {
                params: {
                    container: this.name,
                }
            }).then(response => {
                // console.log(response)
            })
          // console.log(this.id)
          // console.log(response.data.result)
        })

      })

    },

    killContainer() {

      this.axios.get('/api/docker/kill_port').then(response => {

        this.axios.get('/api/docker/kill_container', {
          params: {
            id_name: this.id,
          }
        }).then(response => {
          this.update()

        })

      })

    },

    update() {
      //after hit the button, re-render the status and ip address
      this.axios.get("/api/docker/inspect_container", {
        params: {
          id_name: this.id
        }
      }).then(response => {
        var inspect = JSON.parse(response.data.result)['return']
        // inspect = JSON.parse(inspect)
        var status = inspect['State']['Status']
        this.status = status
        var ip = inspect['NetworkSettings'].IPAddress
        this.ip = ip
        this.setBtn(status)

      });
    },

    goConsole(id) {
      this.port_listening = 'yes'
      //
      this.axios.get('/api/docker/kill_port').then(response => {
        // console.log(response)

        this.axios.get('/api/docker/console_container', {
          params: {
            container_id: id
          }
        }).then(response => {
          // console.log('response', response)
          // this.reload()
        })

      })

      // var path = '/#/ucpe/123/vnfs/dockercontainer?short_id=' + this.short_id
      // var path = 'file:///home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/index.html'
      // var path = 'https://www.google.com'
      // var path = 'file:///home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/index.html'
      // var path = 'file:///home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/index.html'
      // window.open(path)

      // console.log(id)
      // document.getElementById("console").innerHTML = '<object type="text/html" data="hello.html" ></object>';


    },
    stopConsole() {
      this.axios.get('/api/docker/kill_port').then(response => {
        // console.log(response)
        this.reload()
      })
    },

    setBtn(status) {
      if (status == 'exited') {
        document.getElementById("start").removeAttribute("disabled");
        document.getElementById("stop").removeAttribute("disabled");
        document.getElementById("kill").removeAttribute("disabled");
        document.getElementById("restart").removeAttribute("disabled");
        document.getElementById("pause").removeAttribute("disabled");
        document.getElementById("remove").removeAttribute("disabled");

        document.getElementById("stop").setAttribute("disabled", true);
        document.getElementById("kill").setAttribute("disabled", true);
        document.getElementById("restart").setAttribute("disabled", true);
        document.getElementById("pause").setAttribute("disabled", true);

      } else if (status == 'running') {
        document.getElementById("start").removeAttribute("disabled");
        document.getElementById("stop").removeAttribute("disabled");
        document.getElementById("kill").removeAttribute("disabled");
        document.getElementById("restart").removeAttribute("disabled");
        document.getElementById("pause").removeAttribute("disabled");

        document.getElementById("start").setAttribute("disabled", true);
        document.getElementById("restart").setAttribute("disabled", true);
        document.getElementById("remove").setAttribute("disabled", true);
      } else if (status == 'paused') {
        document.getElementById("start").removeAttribute("disabled");
        document.getElementById("stop").removeAttribute("disabled");
        document.getElementById("kill").removeAttribute("disabled");
        document.getElementById("restart").removeAttribute("disabled");
        document.getElementById("pause").removeAttribute("disabled");

        document.getElementById("start").setAttribute("disabled", true);
        document.getElementById("pause").setAttribute("disabled", true);
        document.getElementById("remove").setAttribute("disabled", true);

      }
    },

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
