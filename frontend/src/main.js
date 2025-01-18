import { createApp } from 'vue';
import App from './App.vue';
import router from './router.js';  // Import the router correctly

const app = createApp(App);
app.use(router);  // Use the router with the app instance
app.mount('#app');
