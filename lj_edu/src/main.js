// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import "element-ui/lib/theme-chalk/index.css"
import axios from "axios";
import settings from "./settings";
import "../static/css/global.css"

import "../static/js/gt";

Vue.prototype.$settings = settings
Vue.prototype.$axios = axios
Vue.use(ElementUI)
Vue.config.productionTip = false

require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'
import store from "./store/index";

Vue.use(VideoPlayer);

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: {App},
    template: '<App/>',
    store,
})
