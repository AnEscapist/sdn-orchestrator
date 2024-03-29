import axios from 'axios';
import docker from './modules/docker'
import vms from './modules/vms'
import requestVMList from './modules/vms'

//don't make add things to state, mutations, actions
const state = {}; //empty declaration necessary for getters

const getters = {
  // vnfList: (state, getters, rootstate) => rootstate.vnfs.vms.vmList.concat(rootstate.vnfs.docker.containerList),
  vnfList: (state, getters, rootstate) => rootstate.vnfs.vms.vmList.concat([]),
  vnfCount: (state, getters, rootstate) => {
    // return rootstate.vnfs.vms.vmList.length + rootstate.vnfs.docker.containerList.length
    return rootstate.vnfs.vms.vmList.length - 1; //because of agent
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
