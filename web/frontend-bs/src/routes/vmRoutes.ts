import VM from '../views/vms/VMs.vue';
import Dashboard from '../views/vms/VMDashboard.vue';
import VMContainer from '../views/vms/VMContainer.vue';
import VMHome from '../views/vms/VMHome.vue'
import VMImage from '../views/vms/VMImage.vue'

const vmRoutes =  [
    {
        path: '/vms',
        name: 'virtual machines',
        redirect: '/vms/vmhome',
        component: VM,
        children: [
            {
                path: 'vmhome',
                name: 'vmhome',
                component: VMHome,
            },
            {
                path: 'dashboard',
                name: 'dashboard',
                component: Dashboard
            },
            {
                path: 'vmcontainer',
                name: 'vmcontainer',
                component: VMContainer
            },
            {
                path: 'vmimage',
                name: 'vmimage',
                component: VMImage
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

export default vmRoutes
