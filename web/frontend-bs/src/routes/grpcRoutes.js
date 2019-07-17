import DashboardLayout from '../layout/sample-layout/TemplateLayout.vue'
import HostInfo from '../pages/host-data/HostInfo.vue'

const grpcRoutes = [
    {
        path: '/host-info',
        name: 'DashboardLayout',
        redirect: '/host-info/overview',
        children: [
          {
            path: 'overview',
            name: 'HostInfoOverview',
            component: HostInfo
          }
        ]
    }
];

export default grpcRoutes
