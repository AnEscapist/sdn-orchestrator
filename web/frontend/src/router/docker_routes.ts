import Docker from '../views/Docker.vue';
import DockerDashboard from '../views/DockerDashboard.vue';
import DockerContainer from '../views/DockerContainer.vue';
import DockerHome from '../views/DockerHome.vue'
import DockerImage from '../views/DockerImage.vue'

const vm_routes =  [
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
                path: 'dockerdashboard',
                name: 'dockerdashboard',
                component: DockerDashboard
            },
            {
                path: 'dockercontainer',
                name: 'dockercontainer',
                component: DockerContainer
            },
            {
                path: 'dockerimage',
                name: 'dockerimage',
                component: DockerImage
            }
        ]
    },
]

export default vm_routes
