import axios from 'axios';

const state = {
  vmList: []
};

const mutations = {
  SET_VM_LIST(state, payload){
    state.vmList = payload;
    console.log('mutated');
    console.log(payload);
  }
};

const actions = {
  updateVMList({commit}, token){
    axios.get('/api/all_vm_info/' + controller_id + '/' + ucpe_sn).then((response) => {
      console.log(response.data.result.return);
      commit('SET_VM_LIST', response.data.result.return)
    });
    // commit('SET_VM_LIST', methods.requestVMList()) //todo: make this a promise
  }
};

const getters = {
  vmList: state => state.vmList
};

const controller_id = "test-id";
const ucpe_sn = "test-sn";

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
