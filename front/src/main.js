import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

new Vue({
  router,
  data: {
    email: "ponpon@ponpon.com",
    thepwd:"thepassword",
    errors:[{message:""}, 
            {message:""}]
  },
  render: h => h(App)
}).$mount('#app')