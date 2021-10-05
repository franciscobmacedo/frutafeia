import Vue from 'vue'
import Vuex from 'vuex'
import actions from "@/enum";


import availabilityDummy from './availability.json';
import providersDummy from './providers.json';
import productsDummy from './products.json';
import unitsDummy from './units.json';
import rankingDummy from './ranking.json';
import basketDummy from './baskets.json';

Vue.use(Vuex)


export default new Vuex.Store({
  state: {
    availability: availabilityDummy,
    // availability: [],
    providers: providersDummy,
    products: productsDummy,
    units: unitsDummy,
    ranking: rankingDummy,
    baskets: basketDummy,
    action: ''
  },
  mutations: {
    updateAvailability (state, item) {
      const index = state.availability.findIndex(_ => _.id === item.id)
      state.availability[index] = item;
      state.availability = [...state.availability]
      state.action = actions.EDIT
    },
    addAvailability (state, item) {
      state.availability.push(item);
      state.action = actions.ADD
    },
    deleteAvailability (state, item) {
      const index = state.availability.findIndex(_ => _.id === item.id)
      state.availability.splice(index, 1);
      state.availability = [...state.availability]
      state.action = actions.DELETE
    },
    deleteAllAvailability (state) {
      state.availability = []
    },
  },
  actions: {
    editAvailability(context, item){
      console.log(item)
      context.commit('updateAvailability', item)
      // api call to put data
    },
    addAvailability(context, item){
      console.log(item)
      context.commit('addAvailability', item)
      // api call to add data
    },
    deleteAvailability(context, item){
      console.log(item)
      context.commit('deleteAvailability', item)
      // api call to delete data
    },
    deleteAllAvalilability(context){
      context.commit('deleteAllAvailability')
      // api call to delete ALL data
    }
  },
  modules: {
  }
})
