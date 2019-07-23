import DashboardLayout from '../layout/sample-layout/TemplateLayout.vue'

// Admin pages
import BCMdash from '../pages/bcm/BCMdash.vue'
import UserProfile from '../pages/sample-pages/UserProfile.vue'
import TableList from '../pages/sample-pages/TableList.vue'
import Typography from '../pages/sample-pages/Typography.vue'
import Icons from '../pages/sample-pages/Icons.vue'
import Maps from '../pages/sample-pages/Maps.vue'
import Notifications from '../pages/sample-pages/Notifications.vue'
import Upgrade from '../pages/sample-pages/Upgrade.vue'
import Test from '../pages/sample-pages/Test.vue'

const bcmRoutes = [
  {
    path: '/broadcom',
    component: DashboardLayout,
    redirect: '/broadcom/overview',
    children: [
      {
        path: 'overview',
        name: 'Overview',
        component: BCMdash
      },
      {
        path: 'user',
        name: 'User',
        component: UserProfile
      },
      {
        path: 'table-list',
        name: 'Table List',
        component: TableList
      },
      {
        path: 'typography',
        name: 'Typography',
        component: Typography
      },
      {
        path: 'icons',
        name: 'Icons',
        component: Icons
      },
      {
        path: 'maps',
        name: 'Maps',
        component: Maps
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: Notifications
      },
      {
        path: 'test',
        name: 'test',
        component: Test
      },
      {
        path: 'upgrade',
        name: 'Upgrade to PRO',
        component: Upgrade
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
