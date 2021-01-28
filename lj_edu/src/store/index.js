import Vue from "vue"
import Vuex from "vuex"
Vue.use(Vuex)

export default new Vuex.Store({
    stare:{
        cart_length:0,
    },
    mutations:{
        change_length(state,data){
            state.cart_length=data;
        }
    }
})
