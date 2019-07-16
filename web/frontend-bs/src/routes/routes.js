import templateRoutes from './templateRoutes'
// import dockerRoutes from './dockerRoutes'
// import vmRoutes from './vmRoutes'
// import grpcRoutes from './grpcRoutes'
import DashboardLayout from '../layout/template/TemplateLayout.vue'
// GeneralViews
import NotFound from '../pages/template/NotFoundPage.vue'

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/admin/overview'
  },
  ...templateRoutes,
  // ...dockerRoutes,
  // ...vmRoutes,
  // ...dataRoutes,
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
