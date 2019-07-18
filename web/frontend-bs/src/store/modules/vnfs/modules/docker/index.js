import axios from 'axios';

const state = {
  containerList: []
};

const mutations = {
  //ADD_CONTAINER
};

const actions = {
  // addContainer({commit}, token){
  // }
};

const getters = {
  getContainerList({commit}, token){
    return methods.requestContainerList()
  }
};

const methods = {
  requestContainerList(){
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
