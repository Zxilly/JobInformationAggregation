import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';

const isDebug_mode = process.env.NODE_ENV !== 'production'
Vue.config.debug = isDebug_mode
Vue.config.devtools = isDebug_mode
Vue.config.productionTip = isDebug_mode

if(isDebug_mode){
    Vue.prototype.$apiurl = 'http://127.0.0.1:8000'
}


new Vue({
    vuetify,
    render: h => h(App)
}).$mount('#app')
