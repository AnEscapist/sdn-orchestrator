<template>
  <div>
    <table>
      <tr>
        <input type="checkbox" id="jack" value="Jack" v-model="checkedNames">
        <label for="jack">  Jack</label>
        <input type="checkbox" id="john" value="John" v-model="checkedNames">
        <label for="john">  John</label>
        <input type="checkbox" id="mike" value="Mike" v-model="checkedNames">
        <label for="mike">  Mike</label>
      </tr>
      <tr>
        <input type="checkbox" id="jack" value="Jack" v-model="checkedNames">
        <label for="jack">  Jack</label>
        <input type="checkbox" id="john" value="John" v-model="checkedNames">
        <label for="john">  John</label>
        <input type="checkbox" id="mike" value="Mike" v-model="checkedNames">
        <label for="mike">  Mike</label>
      </tr>
    </table>

    <br>
    <span>Checked names: {{ checkedNames }}</span>
    <h1>{{test}}</h1>
  </div>
</template>
<script>
  import axios from 'axios';
  import Table from "../index";
    export default {
        components: {Table},
        data () {
            return{
            checkedNames: [],
                test: "Hello"
            }
        },
        mounted(){
            axios.get('/api/bcm/show_vlans').then((response) => {
                this.test = response.data.result.result
            }).then(()=>{console.log(this.test)})
        }
    }
</script>
