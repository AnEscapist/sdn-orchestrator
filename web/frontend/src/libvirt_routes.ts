import Libvirt from './views/libvirt/Docker.vue';
import Dashboard from './views/libvirt/LibvirtDashboard.vue';
import LibvirtContainer from './views/libvirt/DockerContainer.vue';
import LibvirtHome from './views/libvirt/DockerHome.vue'
import LibvirtImage from './views/libvirt/DockerImage.vue'

libvirt_routes =  [
    {
        path: '/libvirt',
        name: 'libvirt',
        redirect: '/libvirt/dockerhome',
        component: Libvirt,
        children: [
            {
                path: 'libvirthome',
                name: 'libvirthome',
                component: LibvirtHome,
            },
            {
                path: 'dashboard',
                name: 'dashboard',
                component: Dashboard
            },
            {
                path: 'libvirtcontainer',
                name: 'libvirtcontainer',
                component: LibvirtContainer
            },
            {
                path: 'libvirtimage',
                name: 'libvirtimage',
                component: LibvirtImage
            }
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
]

export default libvirt_routes
