const vnfSidebar = {
  color: 'black', //accepted: '', 'blue', 'azure', 'green', 'orange', 'red', 'purple', 'black';
  backgroundImage: 'img/bigdata.jpg', //public/img/sidebar-5.jpg
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
      to: 'docker_n',
      icon: 'fas fa-network-wired',
      text: 'Networking'
    },
    {
      to: 'docker_v',
      icon: 'fas fa-boxes',
      text: 'Volumes'
    },
    // {
    //   to: 'swarm',
    //   icon: 'fas fa-users',
    //   text: 'Swarm'
    // },
    // {
    //   to: 'events',
    //   icon: 'fas fa-history',
    //   text: 'Event'
    // },
    // {
    //   to: 'notifications',
    //   icon: 'fas fa-bell',
    //   text: 'Notifications'
    // },
  ]
}

export default vnfSidebar
