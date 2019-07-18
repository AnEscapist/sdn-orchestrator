import sampleRoutes from './sampleRoutes'
import grpcRoutes from './grpcRoutes'
import vnfRoutes from './vnfRoutes'
import ucpeRoutes from './ucpeRoutes'
import TemplateLayout from '../layout/sample-layout/TemplateLayout.vue'
// GeneralViews
import NotFound from '../pages/sample-pages/NotFoundPage.vue'

const routes = [
  {
    path: '/',
    component: TemplateLayout,
    redirect: '/admin/overview',
  },
  // ...dockerRoutes,
  // ...vmRoutes,
  ...grpcRoutes,
  ...ucpeRoutes,
  // ...vnfRoutes,
  ...sampleRoutes,

  { path: '*', component: NotFound }
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
 function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes
