import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from './components/UserLogin.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import UserDashboard from './components/UserDashboard.vue';
import UserRegister from './components/UserRegister.vue';
import SelectQuiz from './components/SelectQuiz.vue';
import ManageQuiz from './components/ManageQuiz.vue'

const routes = [
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: UserDashboard
  },
  {
    path: '/register',
    name: 'UserRegister',
    component: UserRegister
  },
  {
    path: '/select-quiz',
    name: 'SelectQuiz',
    component: SelectQuiz
  },
  {
    path: '/manage-quiz',
    name: 'ManageQuiz',
    component: ManageQuiz
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
  
];

const router = createRouter({
  history: createWebHistory(),  // Use history mode for cleaner URLs
  routes
});

export default router;  // Export the router instance
