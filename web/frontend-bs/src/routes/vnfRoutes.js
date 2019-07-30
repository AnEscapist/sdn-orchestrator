// import grpcRoutes from ./grpcRoutes
// import vnfRoutes from ./vnfRoutes
import TestComponent from '../components/test/TestComponent'
import VNFLayout from '../layout/vnfs/VNFLayout'
import VNFDashboard from '../pages/vnfs/VNFDashboard'
import VNFImages from '../pages/vnfs/VNFImages'
import dockerRoutes from './dockerRoutes'
import vmRoutes from './vmRoutes'

const vnfRoutes = [
  {
    path: 'vnfs',
    // path: '/vnfs',
    component: VNFLayout,
    redirect: 'vnfs/home',
    // redirect: '/vnfs/home',
    children: [
      {
        path: 'home',
        name: 'VNF Dashboard',
        component: VNFDashboard
      },
      {
        path: 'images',
        name: 'VNF Images',
        component: VNFImages
      },
      ...dockerRoutes,
      ...vmRoutes
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

export default vnfRoutes
