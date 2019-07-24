// import grpcRoutes from ./grpcRoutes
// import vnfRoutes from ./vnfRoutes
import TestComponent from '../components/test/TestComponent'
import VNFLayout from '../layout/vnfs/VNFLayout'
import VNFDashboard from '../pages/vnfs/VNFDashboard'
import DockerC from '../pages/vnfs/docker/docker_c'
import DockerI from '../pages/vnfs/docker/docker_i'
import DockerV from '../pages/vnfs/docker/docker_v'
import Blank from '@/components/Blank'
import DockerContainer from '../pages/vnfs/docker/dockercontainer'
import DockerImage from '../pages/vnfs/docker/dockerimage'
import DockerVolume from '../pages/vnfs/docker/dockervolume'
import ConsoleContainer from '../pages/vnfs/docker/consolecontainer'

const dockerRoutes = [{
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
    path: 'docker_v',
    name: 'docker_v',
    component: DockerV,
  },
  {
    path: 'dockercontainer',
    name: 'dockercontainer',
    component: DockerContainer,

  },

  {
    path: 'consolecontainer',
    name: 'consolecontainer',
    component: ConsoleContainer,
  },

  {
    path: 'dockerimage',
    name: 'dockerimage',
    component: DockerImage
  },
  {
    path: 'dockervolume',
    name: 'dockervolume',
    component: DockerVolume,
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
