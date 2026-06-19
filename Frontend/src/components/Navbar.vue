<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">
    <div class="container">

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          
        <template v-if="userRole === 'admin'">
            <li class="nav-item"><router-link class="nav-link" to="/admin">Admin Dashboard</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/approvals">Approvals</router-link></li>
            <li class="nav-item" style="position:relative;left:680px">
                <form class="d-flex" role="search" @submit.prevent="search">
                    <input class="form-control me-2" type="search" placeholder="Search" v-model="query" aria-label="Search"/>
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </li>        
        </template>

          <template v-else-if="userRole === 'company' ">
            <li class="nav-item"><router-link class="nav-link" to="/company">Company Dashboard</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/company/profile">My Profile</router-link></li>
          </template>

          <template v-else-if="userRole === 'student'">
            <li class="nav-item"><router-link class="nav-link" to="/student/">Home</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/student/profile">My Profile</router-link></li>
            <li class="nav-item" style="position:relative;left:680px">
                <form class="d-flex" role="search" @submit.prevent="search">
                    <input class="form-control me-2" type="search" placeholder="Search" v-model="query" aria-label="Search"/>
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
              
            </li>  
            <li class="nav-item"><router-link class="nav-link" to="/student/history">My Applications</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/student/offer-letters">Offer Letters</router-link></li>
         </template>
          <template v-else>
              <li class="nav-item"><router-link class="nav-link" to="/">Home</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/student/register">Register</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/company/register">Employer Sign Up</router-link></li>

          </template>

        </ul>

        <div class="navbar-nav">
          <button v-if="isLoggedIn" @click="logout" class="btn btn-outline-danger btn-sm">Logout</button>
          <li v-else class="nav-link"><router-link class="nav-link" to="/login">Login</router-link></li>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import router from '@/router';

export default {
  data() {
    return {
      query:'',
      userRole: localStorage.getItem('role'),
      isLoggedIn: !!localStorage.getItem('token')
    }
  },
  watch: {  // to change routes for different users
    '$route'() {
      this.userRole = localStorage.getItem('role');
      this.isLoggedIn = !!localStorage.getItem('token');
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.userRole = null;
      this.isLoggedIn = false;
      this.$router.push('/login');
    },
    search(){
      if(this.query.trim()){
        this.$router.push({
          path:'/admin',
          query :{q:this.query}
        });
        this.query='';
      }
    }
  }
}
</script>


