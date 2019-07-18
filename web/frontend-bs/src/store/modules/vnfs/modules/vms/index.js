import axios from 'axios';

const state = {
  vmList: []
};

const mutations = {
  SET_VM_LIST(state, payload){
    state.vmList = payload;
  }
};

const actions = {
  updateVMList({commit}, token){
    commit('SET_VM_LIST', methods.requestVMList()) //todo: make this a promise
  }
};

const getters = {
  vmList: state => state.vmList
};

const methods = {
  requestVMList()  {
    return [{'name': 'vm1', 'cpus':2}, {'name': 'vm2', 'cpus':4}]
  },
};

const vmModule = {
  state,
  mutations,
  actions,
  getters,
  methods
};

export default vmModule;
