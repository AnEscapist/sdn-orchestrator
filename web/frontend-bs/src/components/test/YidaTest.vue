<template>
<div>
  <table width='48%'>

    <card>
      <table>
        <tr>
          <td>
            <font-awesome-icon :icon="['fas', 'gamepad']" size=lg color='rgb(111, 111, 111)' />
            <strong> Internet Behavior Control VNF</strong>
          </td>
          <td align='right' width='50%'>
            <button type="button" class="btn btn-primary" @click='go_DPI()'>DPI</button>
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td>
            <div class="input-group mb-3">
              <input v-model='block_list_str' type="text" class="form-control" placeholder="e.g. facebook, youtube, github" aria-label="Recipient's username" aria-describedby="basic-addon2">
              <div class="input-group-append">
                <button type="button" class="btn btn-primary" @click='add_list(block_list_str)'>Add</button>
              </div>
            </div>
          </td>
        </tr>
      </table>

      <card>
        <table width='100%'>
          <tr v-for='(item, i) in block_list'>
            <td width='40%'>
              <h6>{{item}}</h6>
            </td>
            <td width='30%'>
              <toggle-button v-model="status_list[i]" :labels="{checked: 'block', unchecked: 'unblock'}" :width='72' :height='25' />
            </td>
            <td align='right'><button @click='remove_list(i)' type="button" class="btn btn-danger btn-sm">Remove</button></td>
            <hr>
          </tr>
        </table>
        <hr>
        <table width='100%'>
          <tr>
            <td align='right'><button type="button" class="btn btn-primary">Submit</button></td>
          </tr>
        </table>
    </card>

    </card>

<!--
    <router-link to="http://10.10.81.8:8080/dpi">
        <card>
          <table>
            <tr>
              <td>
                <font-awesome-icon :icon="['fas', 'gamepad']" size=lg color='rgb(111, 111, 111)' />
                <strong> Internet Behavior Control VNF</strong>
              </td>
              <td align='right' width='50%'>
                <button type="button" class="btn btn-primary" @click='go_DPI()'>DPI</button>
              </td>
            </tr>
          </table>
          <hr>
        </card>

    </router-link> -->



  </table>



</div>
</template>

<script>
import Card from '@/components/Cards/Card.vue'

import {
  ToggleButton
} from 'vue-js-toggle-button'
export default {
  name: "YidaTest",
  components: {
    Card,
    ToggleButton,
  },
  data: function() {
    return {
      block_list_str: '',
      block_list: ['facebook', 'youtube', 'github'],
      status_list: [true, false, true]
    }


  },
  mounted() {

  },
  methods: {
    // add_list(block_list_str) {
    //   if (block_list_str != '') {
    //     var res = block_list_str.split(',')
    //     var i;
    //     for (i = 0; i < res.length; i++) {
    //       this.block_list.push(res[i].trim())
    //       this.status_list.push(true)
    //     }
    //   }
    //
    // },
    //
    // remove_list(i) {
    //   console.log(i)
    //   this.block_list.splice(i, 1)
    // },

    go_DPI() {
      this.axios.get('/api/docker/go_dpi').then(response => {
        // console.log(response)
      })
    }

  },



}
</script>

<style scoped>
a {
  font-size: 20px;
  font-weight: bold;
  color: rgb(68, 68, 68);
}

.container-fluid {
  /* background: red; */
  /* width: 90%; */
  /* margin-left: 10px; */
  /* margin-right: 10px; */
  padding-top: 15px;
  margin-bottom: 12px;
  border: 1px solid rgb(226, 226, 226);
  border-radius: 4px;
}

.container-fluid:hover {
  background: rgb(240, 240, 240);
}
</style>
