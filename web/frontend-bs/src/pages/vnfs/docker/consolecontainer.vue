<template>
<div class="content">
  <div class="container-fluid">
    <card>
        hello
      <div id="console"></div>
    </card>

  </div>
</div>
</template>

<script>
// import '/home/att-pc-7/Zhengqi/Project/sdn-orchestrator/web/docker-browser-console/bundle.js'
import Card from '@/components/Cards/Card.vue'
export default {
  name: "ConsoleContainer",
  data: {}
}
</script>

<style scoped>
#console {
  /* background: red; */
  position: absolute;
  left: 100px;
  right: 0px;
  top: 0px;
  bottom: 0px;
  padding: 100px;
}

.docker-browser-console .terminal-cursor {
  background-color: #ccc;
}

.docker-browser-console {
  font-family: monospace;
  background-color: black;
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
