// import grpcRoutes from ./grpcRoutes
// import vnfRoutes from ./vnfRoutes

const ucpeRoutes = [
  {
    path: '/ucpe/:ucpe-sn',
    // component: DashboardLayout,
    // redirect: '/ucpe/home',
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
