import DashboardLayout from '../layout/sample-layout/TemplateLayout.vue'

// Admin pages
import BCMdash from '../pages/bcm/BCMdash.vue'

const bcmRoutes = [
  {
    path: '/bcm',
    component: DashboardLayout,
    redirect: '/bcm/overview',
    children: [
      {
        path: 'overview',
        name: 'BCMOverview',
        component: BCMdash
      }
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

export default bcmRoutes
