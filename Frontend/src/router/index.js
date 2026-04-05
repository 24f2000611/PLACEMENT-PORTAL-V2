import { createRouter, createWebHistory } from 'vue-router'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // authentication routes
    {
      'path':'/login',
      'name':'login',
      'component':()=>import('../views/Login.vue')
    },
     {
      'path':'/company/register',
      'name':'company-register',
      'component':()=>import('../views/Company_reg.vue')
    },
      {
      'path':'/student/register',
      'name':'student-register',
      'component':()=>import('../views/Student_reg.vue')
    },
    



    // student routes
    {
      'path':'/student',
      'name':'student-dashboard',
      'component':()=>import('../views/Student.vue')
    },

    {
      'path':'/student/profile',
      'name':'student-profile',
      'component':()=>import('../views/studentProfile.vue')
    },
    




    // admin routes
    {
      'path':'/admin',
      'name':'admin-dashboard',
      'component':()=>import('../views/admin.vue')
    },
    {
      'path':'/admin/approvals',
      'name':'admin-approvals',
      'component':()=>import('../views/approvals.vue')
    },

    {
      'path':'/admin/search',
      'name':'admin-search',
      'component':()=>import('../views/admin.vue')
    },

    
    


    // company routes
     {
      'path':'/company',
      'name':'company-dashboard',
      'component':()=>import('../views/company.vue')
    },

    {
      'path':'/company/profile',
      'name':'company-profile',
      'component':()=>import('../views/companyProfile.vue')
    },

    {
      'path':'/company/drive/info/:id',
      'name':'company-drive-info',
      'component':()=>import('../views/DriveInfo.vue')
    },
    

  ],
})

export default router


//  ROUTES OF ALL THE .VUE PAGES

