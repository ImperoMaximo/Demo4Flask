import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// import '@mdi/font/css/materialdesignicons.css'            
// import { aliases, mdi } from 'vuetify/iconsets/mdi'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
})

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

// Expose backend base URL from Vite env to components as `$back_api_base_url`
console.log(`Using backend API base URL: ${import.meta.env.VITE_BACK_API_BASE_URL}`)
// fallback mais pas vraiment utile sauf en local
const BACK_API = import.meta.env.VITE_BACK_API_BASE_URL || 'http://127.0.0.1:5000'

app.config.globalProperties.$back_api_base_url = BACK_API

app.mount('#app')
