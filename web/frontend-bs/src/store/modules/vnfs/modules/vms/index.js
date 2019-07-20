import axios from 'axios';

const state = {
  vmList: [],
  vmInfo: {}
};

const mutations = {
  SET_VM_LIST(state, payload){
    state.vmList = payload;
  },
  SET_VM_INFO(state, payload){
    state.vmInfo = payload;
  }
};

const controller_id = "test-id";
const ucpe_sn = "test-sn";

const actions = {
  updateVMList({commit}, token){
    // axios.get('/api/all_vm_info/' + controller_id + '/' + ucpe_sn).then((response) => {
    //   commit('SET_VM_LIST', response.data.result.return)
    // });
    // commit('SET_VM_LIST', methods.requestVMList()) //todo: make this a promise
  },
  updateVMInfo({commit}, token){
      axios.get('/api/all_vm_info/' + controller_id + '/' + ucpe_sn).then((response) => {
        commit('SET_VM_INFO', response.data.result.return)}
      )
  }
};

const getters = {
  vmList: state => state.vmList,
  vmInfo: state => state.vmInfo
};


const methods = {
  // requestVMList()  {
  //     axios.get('/api/all_vm_info/' + controller_id + '/' + ucpe_sn).then((response) => {
  //       commit('SET_VM_LIST', response.data)
  //     });
  // },
};

const vmModule = {
  state,
  mutations,
  actions,
  getters,
  methods
};

export default vmModule;
