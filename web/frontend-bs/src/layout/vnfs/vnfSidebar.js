const vnfSidebar = {
  color: 'black', //accepted: '', 'blue', 'azure', 'green', 'orange', 'red', 'purple', 'black';
  backgroundImage: 'img/sidebar-5.jpg', //public/img/sidebar-5.jpg
  items: [
    {
      to: '/vnfs/home',
      icon: 'fas fa-tachometer-alt', //font awesome icon you're welcome;
      text: 'Dashboard'
    },
    {
      to: '/vnfs/images',
      icon: 'fas fa-clone',
      text: 'Images'
    },
    {
      to: '/vnfs/table-list',
      icon: 'fas fa-network-wired',
      text: 'Networking'
    },
    {
      to: '/vnfs/typography',
      icon: 'fas fa-boxes',
      text: 'Volume'
    },
    {
      to: '/vnfs/icons',
      icon: 'fas fa-users',
      text: 'Swarm'
    },
    {
      to: '/vnfs/icons',
      icon: 'fas fa-history',
      text: 'Event'
    },
    {
      to: '/vnf/notifications',
      icon: 'fas fa-bell',
      text: 'Notifications'
    },
  ]
}

export default vnfSidebar
