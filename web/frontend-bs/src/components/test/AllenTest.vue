<template>
  <div>
    <table>
      <tr>
        <!-- Check All -->
        <input type='checkbox' @click='checkAll()' v-model='isCheckAll'> Check All

        <!-- Checkboxes list -->
        <ul>
          <li v-for='lang in langsdata'>
            <input type='checkbox' v-bind:value='lang' v-model='languages' @change='updateCheckall()'>{{ lang }}
          </li>
        </ul>

        <!-- Print -->
        <input type='button' @click='printValues()' value='Print Selected Values'>

        <br>
        Selected items : {{ selectedlang }}

        <!--        <td>-->
        <!--          <input type="checkbox" id="jack" value="Jack" v-model="checkedNames">-->
        <!--          <label for="jack">  Bob</label>-->
        <!--        </td>-->
        <!--        <td>-->
        <!--          <input type="checkbox" id="john" value="John" v-model="checkedNames">-->
        <!--          <label for="john">  John</label>-->
        <!--        </td>-->
        <!--        <td>-->
        <!--          <input type="checkbox" id="mike" value="Mike" v-model="checkedNames">-->
        <!--          <label for="mike">  Mike</label>-->
        <!--        </td>-->
        <!--      </tr>-->
        <!--      <tr>-->
        <!--        <th>-->
        <!--          <input type="checkbox" id="jack" value="Jack"  onclick="selectAll()" v-model="checkedNames">-->
        <!--          <label for="jack"> Select all </label>-->
        <!--        </th>-->
        <!--        <td>-->
        <!--          <input type="checkbox" id="jack" value="Jack" v-model="checkedNames">-->
        <!--          <label for="jack"> Long name </label>-->
        <!--        </td>-->
        <!--        <td>-->
        <!--          <input type="checkbox" id="john" value="John" v-model="checkedNames">-->
        <!--          <label for="john">  John</label>-->
        <!--        </td>-->
        <!--        <td>-->
        <!--          <input type="checkbox" id="mike" value="Mike" v-model="checkedNames">-->
        <!--          <label for="mike">  Mike</label>-->
        <!--        </td>-->
      </tr>
    </table>

    <!--    <br>-->
    <!--    <span>Checked names: {{ checkedNames }}</span>-->
    <!--    <h1>{{test}}</h1>-->
  </div>
</template>
<script>
    import axios from 'axios';
    import Table from "../index";

    export default {
        components: {Table},
        data() {
            return {
                checkedNames: [],
                test: "Hello",
                isCheckAll: false,
                langsdata: ["ge1","ge2","ge3","ge4","ge5","ge6","ge7","ge8","ge9","ge10",
                            "ge11","ge12","ge13","ge14","ge15","ge16","ge17","ge18","ge19","ge20"],
                languages: [],
                selectedlang: ""
            }
        },
        // mounted() {
        //     axios.get('/api/bcm/show_vlans').then((response) => {
        //         this.test = response.data.result.result
        //     }).then(() => {
        //         console.log(this.test)
        //     })
        // },
        methods: {
            checkAll: function () {

                this.isCheckAll = !this.isCheckAll;
                this.languages = [];
                if (this.isCheckAll) { // Check all
                    for (var key in this.langsdata) {
                        this.languages.push(this.langsdata[key]);
                    }
                }
            },
            updateCheckall: function () {
                if (this.languages.length == this.langsdata.length) {
                    this.isCheckAll = true;
                } else {
                    this.isCheckAll = false;
                }
            },
            printValues: function(){
                this.selectedlang = "";
                // Read Checked checkboxes value
                for (var key in this.languages) {
                    this.selectedlang += this.languages[key]+", ";
                }
            }
        }
    }
</script>
