// import grpcRoutes from ./grpcRoutes
// import vnfRoutes from ./vnfRoutes
import TestComponent from '../components/test/TestComponent'
import VNFLayout from '../layout/vnfs/VNFLayout'
import VNFDashboard from '../pages/vnfs/VNFDashboard'
import DockerC from '../pages/vnfs/docker/docker_c'
import DockerI from '../pages/vnfs/docker/docker_i'
import Blank from '@/components/Blank'
import DockerContainer from '../pages/vnfs/docker/dockercontainer'
const dockerRoutes = [
  {
    path: 'docker_c',
    // path: '/vnfs',
    name: 'docker_c',
    component: DockerC,
    // redirect: '/vnfs/home',
    // children: [
    //   {
    //       path: 'dockercontainer',
    //       name: 'dockercontainer',
    //       component: DockerContainer
    //   }
    // ]
  },
  {
    path: 'docker_i',
    name: 'docker_i',
    component: DockerI,
  },
  {
      path: 'dockercontainer',
      name: 'dockercontainer',
      component: DockerContainer,

  }
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
