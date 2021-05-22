// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
// 1. Define route components.
// These can be imported from other files
const Foo = { template: '<div>foooooooooo</div>' }
const Bar = { template: '<div>bar</div>' }

// 2. Define some routes
// Each route should map to a component. The "component" can
// either be an actual component constructor created via
// `Vue.extend()`, or just a component options object.
// We'll talk about nested routes later.
const routes = [
    { path: '/foo', component: Foo },
    { path: '/bar', component: Bar }
  ]
  
  // 3. Create the router instance and pass the `routes` option
  // You can pass in additional options here, but let's
  // keep it simple for now.
  const router = new VueRouter({
    routes // short for `routes: routes`
  })

// 4. Create and mount the root instance.
// Make sure to inject the router with the router option to make the
// whole app router-aware.
const app = new Vue({
    data: {
        todos: [
            { label: 'FRA_GER', cost: 6 },
            { label: 'ENG_GER', cost: 2 },
            { label: 'LUX_BRA', cost: 8 }
        ],
        isConnected: false
    },
    router
  }).$mount('#app')

/*  
const app = new Vue({
        el: '#app',
        data: {
            todos: [
                { label: 'FRA_GER', cost: 6 },
                { label: 'ENG_GER', cost: 2 },
                { label: 'LUX_BRA', cost: 8 }
            ]
        }
    })*/