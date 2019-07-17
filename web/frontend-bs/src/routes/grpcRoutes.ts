import DashboardLayout from '../layout/template/TemplateLayout.vue'
import HostInfo from '../pages/host-data/HostInfo.vue'
import LibvirtHome from "*.vue";

const grpcRoutes = [
    {
        path: '/host-info',
        name: 'DashboardLayout',
        redirect: '/host-info/home',
        children: [
          {
            path: 'overview',
            name: 'HostInfoOverview',
            component: HostInfo
          }
        ]
    }
]

export default grpcRoutes
