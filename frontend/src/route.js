import {createWebHistory, createRouter} from 'vue-router';
import loginUser from './components/user.vue';
import registerUser from './components/register.vue';
import loginForm from './components/login.vue';
import adminHome from './components/home.vue';
import userHome from './components/userHome.vue';
import adminAccess from './components/adminAccess.vue';
import userIssuedBook from './components/userIssuedBook.vue';
import adminSummary from './components/adminSummary.vue';
import userSummary from './components/userSummary.vue';





const routes = [
    {
        
        name: 'adminHome',
        path: '/admin_dashboard/home',
        component: adminHome,
    },
    {
        
        name: 'adminAccess',
        path: '/admin_dashboard/access',
        component: adminAccess,
    },
    {
        
        name: 'userHome',
        path: '/user/dashboard/home',
        component: userHome,
    },
    {
        
        name: 'userIssuedBook',
        path: '/user/dashboard/issued',
        component: userIssuedBook,
    },
    {
        
        name: 'LoginForm',
        path: '/',
        component: loginForm

    },
    {
        name: 'loginUser',
        path: '/user',
        component: loginUser

    },
    {
        name: 'registerUser',
        path: '/register',
        component: registerUser

    },
    {
        name: 'adminSummary',
        path: '/admin_dashboard/summary',
        component: adminSummary
    },
    {
        name: 'userSummary',
        path: '/user/dashboard/summary',
        component: userSummary
    }


];

const router = createRouter({
    history:createWebHistory(),
    routes
});

export default router;
