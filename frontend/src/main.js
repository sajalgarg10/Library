
import { createApp } from 'vue'
import App from './App.vue'
import router from './route';
import vueApexcharts from "vue3-apexcharts";

import 'bootstrap/dist/css/bootstrap.min.css'
//.use(router)
const app = createApp(App)
app.use(router);
app.use(vueApexcharts)
app.mount('#app')
