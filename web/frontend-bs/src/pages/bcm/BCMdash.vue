<template>
  <div class="content">
    <div class="container-fluid">
      <AllenTest></AllenTest>
<!--      todo: notifications fo VNF status changes-->
    </div>
  </div>
</template>

<script>
    import Card from '../../components/Cards/Card.vue'
    import ZhengqiTest from '../../components/test/ZhengqiTest'
    import RogerTest from '../../components/test/RogerTest'
    import AllenTest from "../../components/test/AllenTest";

    export default {
      name: 'BCMdash',
      components: {
        Card, AllenTest
      },
      data () {
        return {
          type: ['', 'info', 'success', 'warning', 'danger'],
          notifications: {
            topCenter: false
          }
        }
      },
      methods: {
        notifyVue (verticalAlign, horizontalAlign) {
          const color = Math.floor((Math.random() * 4) + 1)
          this.$notifications.notify(
            {
              message: `<span>Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer.</span>`,
              icon: 'nc-icon nc-app',
              horizontalAlign: horizontalAlign,
              verticalAlign: verticalAlign,
              type: this.type[color]
            })
        }
      }
    }
</script>

<style scoped>
  .info{
    font-size: 15px;
    padding-left: 10px;
    padding-top: 12px;
    padding-bottom: 12px;
    /*border: 1px solid rgb(180, 180, 180);*/
    /*background: rgb(240, 240, 240);*/
    text-align: left;;
  }
/*todo: consider making this global*/
</style>
