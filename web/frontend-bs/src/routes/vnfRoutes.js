// import grpcRoutes from ./grpcRoutes
// import vnfRoutes from ./vnfRoutes
import TestComponent from '../components/TestComponent'

const vnfRoutes = [
  {
    path: '/vnfs',
    component: TestComponent,
    // redirect: '/home',
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
