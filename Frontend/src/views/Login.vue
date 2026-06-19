<script>
export default {
  data() {
    return {
      formData: {username: '',password: ''},
      message:'',
      messageType:''
    }
  },
  methods: {
    async handleLogin() {
      if (!this.formData.username || !this.formData.password) {
        this.message="Please fill all the details";
        this.messageType="danger";
        return;
      }

      const payload = {
        username: this.formData.username,
        password: this.formData.password
      };

      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload), 
        });

        const data = await response.json();
        
        if (response.ok) {
          localStorage.setItem('token', data.user_details.auth_token);
          localStorage.setItem('role', data.user_details.roles[0]);
          this.message="Login Succesful";
          this.messageType="success";
          
          if (data.user_details.roles[0] === 'student') {
            this.$router.push('/student');
          } 
          else if(data.user_details.roles[0] === 'admin') { 
            this.$router.push('/admin');
          }
          else if(data.user_details.roles[0] === 'company'){
            if(data.user_details.company_profile.approve_status=='Approved'){
              this.$router.push('/company')
            }
            this.message="Wait for admin approval",this.messageType='danger'
          }

        }else {
          this.message=data.message ||"Invalid credentials";
          this.messageType="danger"
        }
      } catch (error) {
        console.error("Network Error:", error);
        this.message="Could not connect to the server.";
        this.messageType="danger";

      }
    } 
  } 
}
</script>

<template>
    <!-- to display the error message -->
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>
  <div class="container ">

    <!-- the login box -->
    <div class="row vh-100 align-items-center justify-content-center d-flex ">
      <div class="col-md-4 card p-4 shadow-sm">
        <h2 class="text-center mb-4">Login</h2>
        
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" v-model="formData.username" class="form-control" placeholder="Enter username">
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="formData.password" class="form-control" placeholder="Enter password">
        </div>

        <button @click="handleLogin" class="btn btn-success w-100">Login</button>
        
        <p class="mt-3 text-center">
          New user? <router-link to="/student/register">Register here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>


