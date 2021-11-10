import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlay  } from '@fortawesome/free-solid-svg-icons'
import { faHeart , faBookmark } from '@fortawesome/free-regular-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faPlay)
library.add(faHeart , faBookmark)

createApp(App).use(router).component('font-awesome-icon', FontAwesomeIcon).mount('#app')