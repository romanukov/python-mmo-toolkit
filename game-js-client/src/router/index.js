import Vue from 'vue'
import VueRouter from 'vue-router'
import LocationsEditor from '../views/LocationsEditor.vue'
import Game from '../views/Game.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'LocationsEditor',
        component: LocationsEditor,
    },
    {
        path: '/game/',
        name: 'Game',
        component: Game,
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
