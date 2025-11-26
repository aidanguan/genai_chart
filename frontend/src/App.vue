<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  height: 100%;
  overflow: hidden;
  margin: 0;
  padding: 0;
}

body {
  height: 100%;
  overflow: hidden;
  margin: 0 !important;
  padding: 0 !important;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  color: #1f2937;
  background: #f3f6fc;
}

#app {
  height: 100vh;
  overflow: hidden;
  margin: 0;
  padding: 0;
}
</style>
