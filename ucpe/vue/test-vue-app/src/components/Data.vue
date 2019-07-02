<template>
  <div class="data">
    <input type="text" v-model="message"/>
    <button @click="emitEvent">emit</button>
  </div>
</template>

<script>
export default {
  name: 'Data',
  data () {
    return {
      message: ''
    }
  },
  sockets: { 
    connect: function () {
      /* eslint-disable no-console */
      console.log('socket connected')
    }
  },
  methods: {
    emitEvent () {
      /* eslint-disable no-console */
      var mess = {"method": "libvirt_controller_get_vm_info", "params": {"body":{"username": "potato", "hostname": "10.10.81.100", "vm_name": "test", "autostart": 1, "save_path": "/home/potato/save_path.test"}}, "jsonrpc": "2.0", "id": 0}
      mess = JSON.stringify(mess)
      this.$socket.emit('get_data', 'hello')
    }
  }
}
</script>

