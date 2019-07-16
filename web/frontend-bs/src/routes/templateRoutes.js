import DashboardLayout from '../layout/template/TemplateLayout.vue'

// Admin pages
import Overview from 'src/pages/template/Overview.vue'
import UserProfile from 'src/pages/template/UserProfile.vue'
import TableList from 'src/pages/template/TableList.vue'
import Typography from 'src/pages/template/Typography.vue'
import Icons from 'src/pages/template/Icons.vue'
import Maps from 'src/pages/template/Maps.vue'
import Notifications from 'src/pages/template/Notifications.vue'
import Upgrade from 'src/pages/template/Upgrade.vue'
import Test from 'src/pages/template/Test.vue'

const templateRoutes = [
  {
    path: '/admin',
    component: DashboardLayout,
    redirect: '/admin/overview',
    children: [
      {
        path: 'overview',
        name: 'Overview',
        component: Overview
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

export default templateRoutes
