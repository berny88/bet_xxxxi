import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isConnected:false,
    u:"",
    p:"",
    errors:[{message:""}, 
            {message:""}]
  },
  mutations: {
    CONNECT(state, isconn) {
        state.isConnected = isconn;
    }
  },
  actions: {
      connect(context, user, pwd) {
        alert("connect "+ user +"/"+ pwd);
        context.state.u=user;
        context.state.p=pwd;
        var isconn=true;
        context.commit('CONNECT', isconn)
      }
  },
  modules: {
    }
})
