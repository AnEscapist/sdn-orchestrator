import Dashboard from '../views/grpc_data_collector/DataDashboard.vue'
import Home from '../views/grpc_data_collector/DataHome.vue'
import LibvirtHome from "*.vue";

const grpc_routes = [
    {
        path: '/data-collect',
        name: 'data-home',
        redirect: '/data-collect/bot',
        component: Home,
    }
]

export default grpc_routes