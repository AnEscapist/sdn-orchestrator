<template>
  <!--  <card>-->
  <!--    <div class="info">-->
  <!--      &lt;!&ndash;      <font-awesome-icon :icon="['fab', 'docker']" size=lg color='rgb(111, 111, 111)' />&ndash;&gt;-->
  <!--      <strong>{{name}}</strong>-->
  <!--      &lt;!&ndash;todo: align badge to the right&ndash;&gt;-->
  <!--      <hr>-->
  <!--      <table>-->
  <!--        <tr>-->
  <!--          <td width='30px'></td>-->
  <!--          <td width='100px'>-->
  <!--            <font-awesome-icon :icon="['fas', 'info-circle']" size=lg color='rgb(111, 111, 111)' />-->
  <!--            <strong> Info: </strong>-->
  <!--          </td>-->
  <!--          <td width='120px'>-->
  <!--            <font-awesome-icon :icon="['fas', 'fire']" size=sm color='rgb(111, 111, 111)' />-->
  <!--            Class: {{functionClass}}-->
  <!--          </td>-->
  <!--          <td width='250px'>-->
  <!--            <font-awesome-icon :icon="['fas', 'file']" size=sm color='rgb(111, 111, 111)' />-->
  <!--            Size: {{filesize}}-->
  <!--            &lt;!&ndash;            todo: add tooltips on hover&ndash;&gt;-->
  <!--          </td>-->
  <!--          <td>-->
  <!--            <font-awesome-icon :icon="['fas', 'microchip']" size=sm color='rgb(111, 111, 111)' />-->
  <!--            16 CPUs-->
  <!--          </td>-->
  <!--        </tr>-->
  <!--        <tr>-->
  <!--          <td width='30px'></td>-->
  <!--          <td width='100px'>-->
  <!--            <font-awesome-icon :icon="['fab', 'linux']" size=lg color='rgb(111, 111, 111)' />-->
  <!--            <strong> OS: </strong>-->
  <!--          </td>-->
  <!--          <td width='250px'>-->
  <!--            {{os}}-->
  <!--          </td>-->
  <!--          &lt;!&ndash;          todo: consider removing host cpu/os (customer knows nothing about docker so doesn't know containers run on host os or even that containers exist)&ndash;&gt;-->
  <!--        </tr>-->
  <!--        <tr>-->
  <!--          <td width='30px'></td>-->
  <!--          <td width='130px'>-->
  <!--            <font-awesome-icon :icon="['fas', 'compass']" size=lg color='rgb(111, 111, 111)' />-->
  <!--            <strong> Description: </strong>-->
  <!--          </td>-->
  <!--          <td width='250px'>-->
  <!--            {{description}}-->
  <!--          </td>-->
  <!--        </tr>-->
  <!--      </table>-->
  <!--    </div>-->
  <!--  </card>-->
  <!--  <card>-->
  <!--  <font-awesome-icon :icon="['fas', 'clone']" size=lg color='rgb(0, 0, 0)' /> <strong> Images</strong>-->
  <!--  <hr>-->

  <!--  <table width="100%">-->
  <!--    <tr>-->
  <!--      <th>Name:tag</th>-->
  <!--      <th>Size</th>-->
  <!--      <th>Created</th>-->
  <!--      <th>Busy</th>-->
  <!--    </tr>-->


  <!--    <tr v-for='(img,i) in all_img' id='containerInfoCard'>-->
  <!--      <router-link :to="{path: 'dockerimage', params: {name: img}, query: {name: img}}">-->
  <!--        <td width='10%'>{{img}}</td>-->
  <!--      </router-link>-->
  <!--      <td width='25%'>{{sizes[i]}}MB</td>-->
  <!--      <td width='25%'>{{createTimes[i]}}</td>-->
  <!--      <td width='10%'>-->
  <!--        &nbsp&nbsp-->
  <!--        <font-awesome-icon v-show="busy[i] == 'yes'" :icon="['fas', 'check-circle']" size=sm color='#00bd56' />-->
  <!--        <font-awesome-icon v-show="busy[i] == 'no'" :icon="['fas', 'times-circle']" size=sm color='rgb(251, 0, 0)' />-->
  <!--      </td>-->
  <!--    </tr>-->
  <!--  </table>-->
  <!--  <hr>-->

  <!--  <button type="button" class="btn btn-primary btn-sm" @click='showPull = !showPull'>-->
  <!--    <font-awesome-icon :icon="['fas', 'cloud-download-alt']" size=sm color='rgb(255, 255, 255)' />-->
  <!--    Pull image-->
  <!--  </button>-->
  <!--  </card>-->
  <!--  <card>-->
  <!--    <div class="pullimage">-->
  <!--      <font-awesome-icon :icon="['fas', 'download']" size=lg />-->
  <!--      <strong> Pull image</strong>-->
  <!--      <hr>-->
  <!--      <div class="pull-choice">-->
  <!--        <table>-->
  <!--          <tr>-->
  <!--            <td>-->
  <!--              <form class="form-inline">-->
  <!--                <strong style="font-size:15px">Image: &nbsp</strong>-->
  <!--                <input type="text" placeholder="e.g. name:tag" v-model="name_tag">-->
  <!--              </form>-->
  <!--            </td>-->

  <!--&lt;!&ndash;            <td>&ndash;&gt;-->
  <!--&lt;!&ndash;              <form class="form-inline">&ndash;&gt;-->
  <!--&lt;!&ndash;                <strong style="font-size:15px">&nbsp Repository: &nbsp</strong>&ndash;&gt;-->
  <!--&lt;!&ndash;                <select v-model='pull_registry' class="custom-select" id="inputGroupSelect01">&ndash;&gt;-->
  <!--&lt;!&ndash;                  &lt;!&ndash; <option selected>Choose...</option> &ndash;&gt;&ndash;&gt;-->
  <!--&lt;!&ndash;                  <option>docker hub</option>&ndash;&gt;-->
  <!--&lt;!&ndash;                  <option>localhost:5000</option>&ndash;&gt;-->
  <!--&lt;!&ndash;                </select>&ndash;&gt;-->
  <!--&lt;!&ndash;              </form>&ndash;&gt;-->
  <!--&lt;!&ndash;            </td>&ndash;&gt;-->
  <!--          </tr>-->
  <!--        </table>-->
  <!--        <br>-->
  <!--        <p class="note">-->
  <!--          <font-awesome-icon :icon="['fas', 'exclamation-triangle']" size=sm color='rgb(249, 194, 0)' />-->
  <!--          Note: if you don't specify the tag of the image, <span class="badge badge-pill badge-info">latest</span> will be used.-->
  <!--        </p>-->
  <!--      </div>-->
  <!--      &lt;!&ndash; <button type="button" class="btn btn-primary" @click="pullImg(name_tag)">-->
  <!--        <font-awesome-icon :icon="['fas', 'cloud-download-alt']" size=sm /> <strong style="font-size:13px"> PULL</strong>-->
  <!--      </button> &ndash;&gt;-->
  <!--      <table>-->
  <!--        <tr>-->
  <!--          <td width='43%'></td>-->
  <!--          <td width='42%'></td>-->
  <!--          <td>-->
  <!--            <button type="button" class="btn btn-secondary btn-sm">-->
  <!--              Cancel-->
  <!--            </button>-->
  <!--          </td>-->
  <!--          <td>-->
  <!--            <button type="button" class="btn btn-primary btn-sm" @click="pullImg(name_tag, pull_registry)">-->
  <!--              <font-awesome-icon :icon="['fas', 'cloud-download-alt']" size=sm /> <strong style="font-size:13px"> PULL</strong>-->
  <!--            </button>-->
  <!--          </td>-->
  <!--        </tr>-->
  <!--      </table>-->
  <!--    </div>-->

  <!--  </card>-->
      <card>
      <table width='100%'>
        <tr>
          <td width='91%'>
            <font-awesome-icon :icon="['fas', 'clone']"
                               size=lg
                               color='rgb(0, 0, 0)'/>
            <strong> Image details - </strong>
            {{imageData.name}}
          </td>
        </tr>
      </table>
      <hr>
      <table width='100%'>
        <tr>
          <td width='20%'>
            <h6>Class</h6>
          </td>
          <td>
            <h6>{{imageData.class}}</h6>
          </td>
        </tr>
      </table>
      <hr>


      <div>
        <!--        <table width='100%'>-->
        <!--          <tr>-->
        <!--            <td width='20%'>-->
        <!--              <h6>ID</h6>-->
        <!--            </td>-->
        <!--            <td>-->
        <!--              <h6>{{image_id}}</h6>-->
        <!--            </td>-->
        <!--          </tr>-->
        <!--        </table>-->
        <!--        <hr>-->
        <!--        <table width='100%'>-->
        <!--          <tr>-->
        <!--            <td width='20%'>-->
        <!--              <h6>Created</h6>-->
        <!--            </td>-->
        <!--            <td>-->
        <!--              <h6>{{created}}</h6>-->
        <!--            </td>-->
        <!--          </tr>-->
        <!--        </table>-->
        <!--        <hr>-->
        <table width='100%'>
          <tr>
            <td width='20%'>
              <h6>Size</h6>
            </td>
            <td>
              <h6>{{imageData.filesize}}</h6>
            </td>
          </tr>
        </table>
        <hr>
        <table width='100%'>
          <tr>
            <td width='20%'>
              <h6>OS</h6>
            </td>
            <td>
              <h6>{{imageData.os}}</h6>
            </td>
          </tr>
        </table>
        <hr>
        <table width='100%'>
          <tr>
            <td width='20%'>
              <h6>Description</h6>
            </td>
            <td>
              <h6>{{imageData.description}}</h6>
            </td>
          </tr>
        </table>
        <hr>
        <!--        <table width='100%'>-->
        <!--          <tr>-->
        <!--            <td width='20%'>-->
        <!--              <h6>CMD</h6>-->
        <!--            </td>-->
        <!--            <td>-->
        <!--              <h6>{{cmd}}</h6>-->
        <!--            </td>-->
        <!--          </tr>-->
        <!--        </table>-->
        <!--        <hr>-->
        <!--        <table width='100%'>-->
        <!--          <tr>-->
        <!--            <td width='20%'>-->
        <!--              <h6>ENV</h6>-->
        <!--            </td>-->
        <!--            <td>-->
        <!--              <h6>{{env}}</h6>-->
        <!--            </td>-->
        <!--          </tr>-->
        <!--        </table>-->
        <!--        <hr>-->
        <table>
          <tr id='containerLinks'>
            <!-- <button type="button" class="btn btn-link">
              <td>
                <font-awesome-icon :icon="['fas', 'trash-alt']" size=sm coler="#1b7fbd" />
                <font size='2px'> Delete</font>
              </td>
            </button> -->
          </tr>
        </table>
      </div>
      </card>
</template>

<script>
  export default {
    name: "VMImage",
    props: [
      'imageData'
    ],
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
