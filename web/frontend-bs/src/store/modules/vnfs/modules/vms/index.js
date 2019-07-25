import axios from 'axios';

const AGENT_NAME = 'agent';

const state = {
  vmList: [],
  vmInfo: {},
  vmSelection: [], //list of vms selected in vm table in vnfs/home
  vmFilterText: '',
  atLeastOneVMSelected: false,
  vmImagesAvailable: [],
  vmCreateForm: {
    vCPUsAvailable: 0,
    memoryAvailable: 0,
    hugepageMemoryAvailable: 0,
  },
  vmBridgesAvailable: [],
  vmWebServerIPV4: ''
};

const mutations = {
  SET_VM_LIST(state, payload) {
    state.vmList = payload;
  },
  SET_VM_INFO(state, payload) {
    state.vmInfo = payload;
  },
  SET_VM_SELECTION(state, payload) {
    state.vmSelection = payload
  },
  SET_VM_FILTER_TEXT(state, payload) {
    state.vmFilter = payload
  },
  SET_AT_LEAST_ONE_VM_SELECTED(state, payload) {
    state.atLeastOneVMSelected = payload
  },
  SET_VCPUS_AVAILABLE(state, payload) {
    state.vmCreateForm.vCPUsAvailable = payload
  },
  SET_MEMORY_AVAILABLE(state, payload) {
    state.vmCreateForm.memoryAvailable = payload
  },
  SET_HUGEPAGE_MEMORY_AVAILABLE(state, payload) {
    state.vmCreateForm.hugepageMemoryAvailable = payload
  },
  SET_VM_IMAGES_AVAILABLE(state, payload) {
    state.vmImagesAvailable = payload
  },
  SET_VM_BRIDGES_AVAILABLE(state, payload) {
    state.vmBridgesAvailable = payload
  },
  SET_VM_WEB_SERVER_IPV4(state, payload){
    state.vmWebServerIPV4 = payload
  }
};

const controller_id = "test-id";
const ucpe_sn = "test-sn";
const URL_PREFIX = `/api/vms/`;
const URL_SUFFIX = `/${controller_id}/${ucpe_sn}`;

const actions = {
  updateVMInfo({ commit }, token) {
    axios.get(getURL('all_vm_info')).then((response) => {
        let vmInfo = response.data.result.return;
        let vmNames = Object.keys(vmInfo);
        commit('SET_VM_INFO', vmNames
          .filter(vmName => vmName !== AGENT_NAME)
          .reduce((obj, vmName) => {
            return {
              ...obj,
              [vmName]: vmInfo[vmName]
            }
          }, {})
        );
        commit('SET_VM_LIST', vmNames)
      }
    ).catch(err => console.log(err))
    // https://stackoverflow.com/questions/38750705/filter-object-properties-by-key-in-es6
  },
  updateVMSelection({ commit }, newSelection) {
    commit('SET_VM_SELECTION', newSelection)
    commit('SET_AT_LEAST_ONE_VM_SELECTED', !!newSelection.length) //!! is a trick to cast to truthiness value bool
  },
  updateVMFilterText({ commit }, newFilterText) {
    commit('SET_VM_FILTER_TEXT', newFilterText)
  },
  startSelectedVMs({ commit, dispatch }) {
    axios.post(getURL('start_or_resume_selected_vms'), { 'vm_names': state.vmSelection }).then((response) => {
      dispatch('updateVMInfo')
    });
  },
  pauseSelectedVMs({ commit, dispatch }) {
    axios.post(getURL('pause_selected_vms'), { 'vm_names': state.vmSelection }).then((response) => {
      dispatch('updateVMInfo')
    });
  },
  killSelectedVMs({ commit, dispatch }) {
    axios.post(getURL('kill_selected_vms'), { 'vm_names': state.vmSelection }).then((response) => {
      dispatch('updateVMInfo')
    });
  },
  deleteSelectedVMs({ commit, dispatch }) {
    axios.post(getURL('delete_selected_vms'), { 'vm_names': state.vmSelection }).then((response) => {
      dispatch('updateVMSelection', []);
      dispatch('updateVMInfo')
    });
  },
  createVM({ commit, dispatch }, form) {
    return axios.post(getURL('create_vm'), { 'form': form }).then((response) => {
      dispatch('updateVMInfo')
    });
  },
  updateVMVCPUsAvailable({ commit }) {
    return axios.get('/api/grpc/cpu_total').then((response) => {
      commit('SET_VCPUS_AVAILABLE', parseInt(response.data.result.return))
    })
  },
  updateVMMemoryAvailable({ commit }) {
    return axios.get('/api/grpc/avail_mem_bytes').then((response) => {
      commit('SET_MEMORY_AVAILABLE', parseMemoryIntGBFromBytes(response.data.result.return))
    })
  },
  updateVMHugepageMemoryAvailable({ commit }) {
    return axios.get('/api/grpc/hugepage_free_mem_bytes').then((response) => {
      commit('SET_HUGEPAGE_MEMORY_AVAILABLE', parseMemoryIntGBFromBytes(response.data.result.return))
    })
  },
  updateVMImagesAvailable({ commit }) {
    return axios.get(getURL('/images')).then((response) => {
      commit('SET_VM_IMAGES_AVAILABLE', response.data.images)
  })
  },
  updateVMBridgesAvailable({ commit }) {
    return axios.get('/api/grpc/linux_bridge_list').then((response) => {
      commit('SET_VM_BRIDGES_AVAILABLE', eval(response.data.result.return)) //solved all of our problems just now
    })
  },
  updateVMWebServerIPV4({commit}){
    return axios.get('/api/utils/ipv4').then((response) => {
      commit('SET_VM_WEB_SERVER_IPV4', response.data.ipv4)
    })
  },
  prepareVMConsole({commit}, vm_name){
    console.log("prepare vm console called")
    return axios.get(getURL('console') + `/${vm_name}`)
  },
};

const getters = {
  vmList: state => state.vmList,
  vmInfo: state => state.vmInfo,
  vmSelection: state => state.vmSelection,
  // vmState: (state, vmName) => state.vmInfo[vmName]["state"]
  vmFilterText: state => state.vmFilterText,
  vmStateFromName: state => (name) => state.vmInfo[name].state,
  vmAtLeastOneSelected: state => state.atLeastOneVMSelected,
  vmCreateForm: state => state.vmCreateForm,
  vmVCPUOptions: state => getOneToNArray(state.vmCreateForm.vCPUsAvailable),
  vmMemoryOptions: state => getOneToNArray(state.vmCreateForm.memoryAvailable),
  vmHugepageMemoryOptions: state => getOneToNArray(state.vmCreateForm.hugepageMemoryAvailable),
  vmImagesAvailable: state => state.vmImagesAvailable,
  vmBridgesAvailable: state => state.vmBridgesAvailable,
  vmWebServerIPV4: state => state.vmWebServerIPV4 //todo: move this to somewhere reasonable
};

function getURL(endpoint) {
  return `${URL_PREFIX}/${endpoint}/${URL_SUFFIX}`;
}

function parseMemoryIntGBFromBytes(memoryStr) {
  //memoryStr: memory in bytes, ex. '12355'
  //return: memory in gigabytes, as an int
  let bytes_in_gigabyte = Math.pow(1024, 3);
  return parseInt((parseInt(memoryStr)/bytes_in_gigabyte));
}

function getOneToNArray(n) {
  return Array.from(Array(n).keys()).map(x => x + 1)
}

const methods = {};

const vmModule = {
  state,
  mutations,
  actions,
  getters,
  methods
};

export default vmModule;
