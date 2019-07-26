import grpcRoutes from './grpcRoutes'
import vnfRoutes from './vnfRoutes'
import DashboardLayout from '../layout/sample-layout/TemplateLayout'
import Blank from '../components/Blank'

const ucpeRoutes = [
  {
    path: '/ucpe/:ucpe_sn',
    component: Blank,
    // redirect: '/ucpe/home', //todo: redirect to list of ucpes
    children: [
      ...grpcRoutes,
      ...vnfRoutes
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

export default ucpeRoutes
