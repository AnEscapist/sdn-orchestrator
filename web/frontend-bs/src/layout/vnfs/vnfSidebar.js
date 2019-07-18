const vnfSidebar = {
  color: 'black', //accepted: '', 'blue', 'azure', 'green', 'orange', 'red', 'purple', 'black';
  backgroundImage: 'img/sidebar-5.jpg', //public/img/sidebar-5.jpg
  items: [
    {
      to: 'home',
      icon: 'fas fa-tachometer-alt', //font awesome icon you're welcome;
      text: 'Dashboard'
    },
    {
      to: 'images',
      icon: 'fas fa-clone',
      text: 'Images'
    },
    {
      to: 'networking',
      icon: 'fas fa-network-wired',
      text: 'Networking'
    },
    {
      to: 'volume',
      icon: 'fas fa-boxes',
      text: 'Volume'
    },
    {
      to: 'swarm',
      icon: 'fas fa-users',
      text: 'Swarm'
    },
    {
      to: 'events',
      icon: 'fas fa-history',
      text: 'Event'
    },
    {
      to: 'notifications',
      icon: 'fas fa-bell',
      text: 'Notifications'
    },
  ]
}

export default vnfSidebar
