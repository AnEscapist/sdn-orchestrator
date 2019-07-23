<template>
<div class="content">
  <div class="container-fluid">
    <card>

      <font-awesome-icon :icon="['fas', 'clone']" size=lg color='rgb(0, 0, 0)' /> <strong> Images</strong>
      <hr>

      <table width="100%">
        <tr>
          <th>Name:tag</th>
          <th>Size</th>
          <th>Created</th>
          <th>Busy</th>
        </tr>


        <tr v-for='(img,i) in all_img' id='containerInfoCard'>
          <router-link :to="{path: 'dockerimage', params: {name: img}, query: {name: img}}">
            <td width='10%'>{{img}}</td>
          </router-link>
          <td width='25%'>{{sizes[i]}}MB</td>
          <td width='25%'>{{createTimes[i]}}</td>
          <td width='10%'>
              &nbsp&nbsp
            <font-awesome-icon v-show="busy[i] == 'yes'" :icon="['fas', 'check-circle']" size=sm color='#00bd56' />
            <font-awesome-icon v-show="busy[i] == 'no'" :icon="['fas', 'times-circle']" size=sm color='rgb(251, 0, 0)' />
          </td>
        </tr>
      </table>
      <hr>
      <div class="pullimage">
        <font-awesome-icon :icon="['fas', 'download']" size=lg />
        <strong> Pull image</strong>
        <hr>
        <div class="pull-choice">
          <table>
            <tr>
              <td>
                <form class="form-inline">
                  <strong style="font-size:15px">Image: &nbsp</strong>
                  <input type="text" placeholder="e.g. name:tag" v-model="name_tag">
                </form>
              </td>

              <td>
                <form class="form-inline">
                  <strong style="font-size:15px">&nbsp Repository: &nbsp</strong>
                  <input type="text" placeholder="docker hub">
                </form>
              </td>
            </tr>
          </table>
          <br>
          <p class="note">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" size=sm color='rgb(249, 194, 0)' />
            Note: if you don't specify the tag of the image, <span class="badge badge-pill badge-info">latest</span> will be used.
          </p>
        </div>
        <button type="button" class="btn btn-primary" @click="pullImg(name_tag)">
          <font-awesome-icon :icon="['fas', 'cloud-download-alt']" size=sm /> <strong style="font-size:13px"> PULL</strong>
        </button>
      </div>
    </card>

  </div>
</div>
</template>

<script>
import Card from '../../../components/Cards/Card.vue'
// import { mapGetters, mapActions } from 'vuex'
// import LTable from '@/components/Table.vue'

export default {
  inject: ['reload'],
  name: 'DockerI',

  components: {
    Card,

  },
  data() {
    return {
      using_images: [],
      // images: [],
      busy: [],
      client: '',
      info: '',
      status: [],
      all_img: [],
      name_tag: '',

      inspect: '',
      sizes: [],
      createTimes: [],
    }
  },
  mounted() {

    this.axios.get("/api/docker/list_images").then(response => {
      var res = JSON.parse(response.data.result)['return']
      var regex = /\<(.+?)\>/g;
      var imgs = res.match(regex)
      var i;
      for (i = 0; i < imgs.length; i++) {
        this.all_img.push(imgs[i].substring(imgs[i].indexOf(':') + 3, imgs[i].indexOf('>') - 1))
      }

      var j;
      for (j = 0; j < this.all_img.length; j++) {
        this.sizes = []
        this.createTimes = []
        this.axios.get('/api/docker/inspect_image', {
          params: {
            name: this.all_img[j]
          }
        }).then(response => {
          var inspect = JSON.parse(response.data.result)['return']
          this.inspect = inspect
          // console.log(inspect)
          this.sizes.push((parseFloat(inspect['Size']) / 1000000).toFixed(1))
          this.createTimes.push(inspect['Created'].split('.')[0].split('T').join(' / '))
        })
      }

      this.busy = []
      this.axios.get('api/docker/containers_images').then(response => {
        var res = JSON.parse(response.data.result)['return']
        var regex = /\<(.+?)\>/g;
        var images = res.match(regex)
        var i;
        for (i = 0; i < images.length; i++) {
          if (!(images[i] in this.using_images)) {
            this.using_images.push(images[i].substring(images[i].indexOf(':') + 3, images[i].indexOf('>') - 1))
          }
        }

        var i;
        for (i = 0; i < this.all_img.length; i++) {

          var str = JSON.stringify(this.using_images)
          if (str.includes(this.all_img[i])) {
            this.busy.push('yes')
          } else {
            this.busy.push('no')
          }
        }
      })



    });

    // this.axios.get('api/docker/containers_images').then(response => {
    //   var res = JSON.parse(response.data.result)['return']
    //   var regex = /\<(.+?)\>/g;
    //   var images = res.match(regex)
    //   var i;
    //   for (i = 0; i < images.length; i++) {
    //     this.images.push(images[i].substring(images[i].indexOf(':') + 3, images[i].indexOf('>') - 1))
    //   }
    // })


  },
  methods: {
    notifyVue(verticalAlign, horizontalAlign) {
      const color = Math.floor((Math.random() * 4) + 1)
      this.$notifications.notify({
        message: `<span>Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer.</span>`,
        icon: 'nc-icon nc-app',
        horizontalAlign: horizontalAlign,
        verticalAlign: verticalAlign,
        type: this.type[color]
      })
    },
    pullImg(name_tag) {
      if (name_tag.includes(':')) {
        var name = name_tag.split(':')[0]
        var tag = name_tag.split(':')[1]
      } else {
        var name = name_tag
        var tag = 'latest'
      }
      this.axios.get('/api/docker/pull_image', {
        params: {
          name: name,
          tag: tag,
          // timeout: 1000
        }
      }).then(response => {
        // console.log(JSON.parse(response.data.result))
        this.reload()
      })

    },
  }
}
</script>

<style scoped>
.info {
  font-size: 15px;
  padding-left: 10px;
  padding-top: 12px;
  padding-bottom: 12px;
  /*border: 1px solid rgb(180, 180, 180);*/
  /*background: rgb(240, 240, 240);*/
  text-align: left;
  ;
}

a {
  color: rgb(38, 138, 255);
  font-family: Arial, sans-serif;
  font-weight: bold;
  font-size: 13px;
}

input {

  border: 2px solid rgb(200, 200, 200);
  border-radius: 4px;
  padding-left: 8px;
}

p {
  font-size: 12px;
  font-weight: bold;
}


#containerInfoCard {
  font-family: Arial, sans-serif;
  font-size: 15px;
  background-color: rgb(248, 248, 248);
  border-bottom: 2px solid white;
  height: 25px;
  padding-top: 3px;
  padding-bottom: 3px;

}

#containerInfoCard:hover {
  background-color: rgb(233, 233, 233);
}

/*todo: consider making this global*/
</style>
