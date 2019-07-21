import axios from 'axios';

const state = {
  vmList: [],
  vmInfo: {},
  vmSelection: [] //list of vms selected in vm table in vnfs/home
};

const mutations = {
  SET_VM_LIST(state, payload){
    state.vmList = payload;
  },
  SET_VM_INFO(state, payload){
    state.vmInfo = payload;
  },
  SET_VM_SELECTION(state, payload){
    state.vmSelection = payload
  }
};

const controller_id = "test-id";
const ucpe_sn = "test-sn";
const URL_PREFIX = '/api/vms';

const actions = {
  updateVMList({commit}, token){
    // axios.get('/api/all_vm_info/' + controller_id + '/' + ucpe_sn).then((response) => {
    //   commit('SET_VM_LIST', response.data.result.return)
    // });
    // commit('SET_VM_LIST', methods.requestVMList()) //todo: make this a promise
  },
  updateVMInfo({commit}, token){
      axios.get(`${URL_PREFIX}/all_vm_info/${controller_id}/${ucpe_sn}`).then((response) => {
        commit('SET_VM_INFO', response.data.result.return)}
      )
  },
  updateVMSelection({commit}, newSelection){
    commit('SET_VM_SELECTION', newSelection)
  },
  startSelectedVMs({commit}){;
    axios.post(`${URL_PREFIX}/start_selected_vms`, {'vm_names': state.vmSelection});
  }
};

const getters = {
  vmList: state => state.vmList,
  vmInfo: state => state.vmInfo,
  vmSelection: state => state.vmSelection
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
