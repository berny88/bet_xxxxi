import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isConnected:false,
    errors:[{message:""}, 
            {message:""}]
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
