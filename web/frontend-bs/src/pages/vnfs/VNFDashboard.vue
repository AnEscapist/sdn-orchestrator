<template>
  <div class="content">
    <div class="container-fluid">
      <VNFSummaryPanel></VNFSummaryPanel>
      <RogerTest></RogerTest>
      <ZhengqiTest></ZhengqiTest>
      <!-- <YidaTest></YidaTest> -->
      <!--      <SampleCard></SampleCard>-->
      <!--      todo: notifications fo VNF status changes-->
    </div>
  </div>
</template>

<script>
  import Card from '../../components/Cards/Card.vue'
  import SampleCard from './SampleCard'
  import VNFSummaryPanel from './VNFSummaryPanel'
  import VNFInfoPanel from './VNFInfoPanel'
  import ZhengqiTest from '../../components/test/ZhengqiTest'
  import RogerTest from '../../components/test/RogerTest'
  import YidaTest from '../../components/test/YidaTest'

  export default {
    name: 'VNFDashboard',
    components: {
      Card, SampleCard, VNFSummaryPanel, VNFInfoPanel, ZhengqiTest, RogerTest, YidaTest
    },
    data() {
      return {
        type: ['', 'info', 'success', 'warning', 'danger'],
        notifications: {
          topCenter: false
        }
      }
    },
    methods: {
      notifyVue(verticalAlign, horizontalAlign) {
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
  .info {
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
