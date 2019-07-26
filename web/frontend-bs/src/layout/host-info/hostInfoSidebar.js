const hostInfoSidebar = {
  color: 'black', //accepted: '', 'blue', 'azure', 'green', 'orange', 'red', 'purple', 'black';
  backgroundImage: 'img/bigdata.jpg', //public/img/sidebar-5.jpg
  items: [
    {
      to: 'overview',
      icon: 'fas fa-tachometer-alt', //font awesome icon you're welcome;
      text: 'Dashboard'
    },
    {
      to: 'network-devices',
      icon: 'fas fa-network-wired',
      text: 'Network Devices'
    },
  ]
}

export default hostInfoSidebar
