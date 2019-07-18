// import grpcRoutes from ./grpcRoutes
// import vnfRoutes from ./vnfRoutes
import TestComponent from '../components/test/TestComponent'
import VNFLayout from '../layout/vnfs/VNFLayout'
import VNFDashboard from '../pages/vnfs/VNFDashboard'
import DockerDashboard from '../pages/vnfs/docker/dockerdashboard'
import DockerContainer from '../pages/vnfs/docker/dockercontainer'
const dockerRoutes = [
  {
    path: 'dockerdashboard',
    // path: '/vnfs',
    component: DockerDashboard,
    redirect: 'vnfs/docker',
    // redirect: '/vnfs/home',
    children: [
      {
        path: 'vnfs/docker/dockercontainer',
        name: 'dockercontainer',
        component: DockerContainer
      },
    ]
  },
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
 function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default dockerRoutes
