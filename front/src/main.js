import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false

new Vue({
  router,

  data: {
    email: "ponpon@ponpon.com",
    thepwd:"thepassword",
    errors:[{message:""}, 
            {message:""}]
  },

  store,
  render: h => h(App)
}).$mount('#app')