import axios from 'axios';

const state = {
  containerList: []
};

const mutations = {
  //ADD_CONTAINER
  SET_CONTAINER_LIST(state, payload){
    state.containerList = payload;
  }
};

const actions = {
  updateContainerList({commit}, token){
    commit('SET_CONTAINER_LIST', methods.requestContainerList())
  }
};

const getters = { //note: these are for retrieving things directly from the state.  DO NOT put backend requests here
  containerList: state => state.containerList
};

const methods = {
  requestContainerList(){ //todo: put axios requests here
    return [{'name': 'con1', 'port':"7001"}, {'name': 'con2', 'port':'7002'}]
  }
};

const dockerModule = {
  state,
  mutations,
  actions,
  getters,
  methods
};

export default dockerModule;
