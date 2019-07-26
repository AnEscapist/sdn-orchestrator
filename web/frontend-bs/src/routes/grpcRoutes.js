import HostInfoLayout from '../layout/host-info/HostInfoLayout.vue'
import HostInfo from '../pages/host-data/HostInfo.vue'
import HostInfoNetworkDevices from "../pages/host-data/HostInfoNetworkDevices";

const grpcRoutes = [
    {
        path: 'host-info',
        name: 'HostInfo',
        component: HostInfoLayout,
        redirect: 'host-info/overview',
        children: [
          {
            path: 'overview',
            name: 'HostInfoOverview',
            component: HostInfo
          },
          {
            path: 'network-devices',
            name: 'HostInfoNetworkDevices',
            component: HostInfoNetworkDevices
          }
        ]
    }
];

export default grpcRoutes
