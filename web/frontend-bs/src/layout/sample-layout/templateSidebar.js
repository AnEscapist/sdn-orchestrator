
const templateSidebar = {
  color: 'black', //accepted: '', 'blue', 'azure', 'green', 'orange', 'red', 'purple', 'black';
    backgroundImage: 'img/sidebar-5.jpg', //public/img/sidebar-5.jpg
    items: [
    {
      to: '/admin/overview',
      // icon: 'nc-icon nc-chart-pie-35',
      icon: 'fas fa-tachometer-alt', //font awesome icon you're welcome;
      text: 'Dashboard'
    },
    {
      to: '/admin/user',
      icon: 'nc-icon nc-circle-09',
      text: 'User Profile'
    },
    {
      to: '/admin/table-list',
      icon: 'nc-icon nc-notes',
      text: 'Table List'
    },
    {
      to: '/admin/typography',
      icon: 'nc-icon nc-paper-2',
      text: 'Typography'
    },
    {
      to: '/admin/icons',
      icon: 'nc-icon nc-atom',
      text: 'Icons'
    },
    {
      to: '/admin/maps',
      icon: 'nc-icon nc-pin-3',
      text: 'Maps'
    },
    {
      to: '/admin/notifications',
      icon: 'nc-icon nc-bell-55',
      text: 'Notifications'
    },
  ]
}

export default templateSidebar
