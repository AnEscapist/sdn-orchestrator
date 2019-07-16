import Dashboard from '../views/grpc_data_collector/DataDashboard.vue'
import Home from '../views/grpc_data_collector/DataHome.vue'
import LibvirtHome from "*.vue";

const grpcRoutes = [
    {
        path: '/data-collect',
        name: 'data-home',
        redirect: '/data-collect/bot',
        component: Home,
    }
]

export default grpcRoutes
