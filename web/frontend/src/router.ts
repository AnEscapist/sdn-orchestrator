import Vue from 'vue';
import Router from 'vue-router';


import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Docker from './views/Docker.vue';
import Dashboard from './views/DockerDashboard.vue';
import DockerContainer from './views/DockerContainer.vue';
import DockerHome from './views/DockerHome.vue'


Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            redirect: '/login',
            component: Home,
        },
        {
            path: '/about',
            name: 'about',
            // route level code-splitting
            // this generates a separate chunk (about.[hash].js) for this route
            // which is lazy-loaded when the route is visited.
            component: () => import(/* webpackChunkName: "about" */ './views/About.vue'),
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
        },
        {
            path: '/docker',
            name: 'docker',
            redirect: '/docker/dockerhome',
            component: Docker,
            children: [
                {
                    path: 'dockerhome',
                    name: 'dockerhome',
                    component: DockerHome,
                },
                {
                    path: 'dashboard',
                    name: 'dashboard',
                    component: Dashboard
                },
                {
                    path: 'dockercontainer',
                    name: 'dockercontainer',
                    component: DockerContainer
                },
                // {
                //     path: 'image',
                //     name: 'image',
                //     component: Image
                // }
            ]
        },
        // {
        //     path: '/dashboard',
        //     name: 'dashboard',
        //     component: Dashboard
        // }
    ],
});
