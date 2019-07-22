import axios from 'axios';

const state = {
  drivers: []
};

const mutations = {
  UPDATE_DRIVERS(state, payload){
    state.drivers = payload
  }
};

const actions = {
  updateDrivers({commit}, token){
    axios.get("/api/grpc/get_net_devices").then((response) => {
      commit('UPDATE_DRIVERS', response.data.result.return)}
    )
  }
};

const getters = { //note: this is for retrieving things from the state.  DO NOT put backend requests here
  drivers: state => state.drivers
};

const methods = { //axios requests go here

};

const hostInfoModule = {
  state,
  mutations,
  actions,
  getters,
  methods
};

export default hostInfoModule;
