import { createRouter, createWebHistory } from 'vue-router'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      'path':'/login',
      'name':'login',
      'component':()=>import('../views/Login.vue')
    },
    {
      'path':'/student/register',
      'name':'student-register',
      'component':()=>import('../views/Student_reg.vue')
    },
     {
      'path':'/company/register',
      'name':'company-register',
      'component':()=>import('../views/Company_reg.vue')
    },
    {
      'path':'/student',
      'name':'student-dashboard',
      'component':()=>import('../views/Student.vue')
    },
    {
      'path':'/admin',
      'name':'admin-dashboard',
      'component':()=>import('../views/admin.vue')
    },
     {
      'path':'/company',
      'name':'company-dashboard',
      'component':()=>import('../views/company.vue')
    },

  ],
})

export default router


//  ROUTES OF ALL THE .VUE PAGES

