import axios from 'axios';
import docker from './modules/docker'
import vms from './modules/vms'
import requestVMList from './modules/vms'

//don't make state, mutations, actions

const getters = {
  VNFList: state => vms.state.vmList.concat(docker.state.containerList)
  VNFCount: state => {
    ret
  }
};

const modules = {
  docker, vms
};

const vnfModule = {
  state,
  mutations,
  actions,
  getters,
  modules
};

export default vnfModule;
