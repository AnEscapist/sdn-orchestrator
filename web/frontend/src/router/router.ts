import Vue from 'vue';
import Router from 'vue-router';


import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Docker from '../views/docker/Docker.vue';
import DockerDashboard from '../views/docker/DockerDashboard.vue';
import DockerContainer from '../views/docker/DockerContainer.vue';
import DockerHome from '../views/docker/DockerHome.vue'
import DockerImage from '../views/docker/DockerImage.vue'
import grpc_routes from './grpc_router'
import vm_routes from "@/router/vm_routes";
import docker_routes from '@/router/docker_routes'

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
            component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
        },
        {
            path: '/login',
            name: 'login',
            component: Login,
        },
        ...docker_routes,
        // ...grpc_routes,
        ...vm_routes
        // {
        //     path: '/dashboard',
        //     name: 'dashboard',
        //     component: Dashboard
        // }
    ],
});
