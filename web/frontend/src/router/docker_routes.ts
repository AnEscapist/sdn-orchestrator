import Docker from '../views/docker/Docker.vue';
import DockerDashboard from '../views/docker/DockerDashboard.vue';
import DockerContainer from '../views/docker/DockerContainer.vue';
import DockerHome from '../views/docker/DockerHome.vue'
import DockerImage from '../views/docker/DockerImage.vue'

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
