import DashboardLayout from '../layout/sample-layout/TemplateLayout.vue'
import HostInfo from '../pages/host-data/HostInfo.vue'
import Test2 from "../pages/host-data/Test2";

const grpcRoutes = [
    {
        path: '/host-info',
        name: 'DashboardLayout',
        component: DashboardLayout,
        redirect: '/host-info/overview',
        children: [
          {
            path: 'overview',
            name: 'HostInfoOverview',
            component: HostInfo
          },
          {
            path: 'test2',
            name: 'Test2',
            component: Test2
          }
        ]
    }
];

export default grpcRoutes
