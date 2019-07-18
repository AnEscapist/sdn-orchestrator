import axios from 'axios';
import docker from './modules/docker'
import vms from './modules/vms'
import requestVMList from './modules/vms'

//don't make add things to state, mutations, actions
const state = {}; //empty declaration necessary for getters

const getters = {
  VNFList: state => vms.state.vmList.concat(docker.state.containerList),
  VNFCount: state => {
    return vms.state.vmList.length + vms.state.containerList.length
  }
};

const modules = {
  docker, vms
};

const vnfModule = {
  state,
  getters,
  modules
};

export default vnfModule;
