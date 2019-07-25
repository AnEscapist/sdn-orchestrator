<template>
<div class="content">
  <div class="container-fluid">
    <card>
        hello
      <div id="console"></div>
      <!-- <div v-html="/home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/index.html"> </div> -->
      <!-- <iframe src="///home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/index.html" scrolling="yes" style="width: 100%;height: 500px;" frameborder="0"></iframe> -->

      <!-- <iframe src='http://www.google.com' scrolling="yes" style="width: 100%;height: 500px;" frameborder="0"></iframe> -->
    </card>

  </div>
</div>
</template>

<script>
// import '/home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/bundle.js'
import Card from '@/components/Cards/Card.vue'
export default {
  name: "ConsoleContainer",

}
</script>

<style scoped>
#console {
    position: absolute;
    left: 0px;
    right: 0px;
    top: 0px;
    bottom: 0px;
    padding: 20px;
}

.docker-browser-console .terminal-cursor {
    background-color: rgb(255, 0, 0);
}

.docker-browser-console {
    padding-left: 20%;
    padding-right: 20%;
    padding-top: 5%;
    padding-bottom: 5%;
    height: 100%;
    font-family: monospace;
    background-color: white;
}

/* .container-fluid {
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

} */
</style>
