import Vue from 'vue'
import Router from 'vue-router'
import Course from "../components/Course";
import Index from "../components/Index";
import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import Detail from "../components/Detail";
import Cart from "../components/Cart";


Vue.use(Router)

export default new Router({
  routes: [
      {path:"/",component:Home},
      {path:"/course",component:Course},
      {path:"/index",component:Index},
      {path:"/login",component:Login},
      {path:"/register",component:Register},
      {path:"/detail/:id",component:Detail},
      {path:"/cart",component:Cart},
  ]
})
