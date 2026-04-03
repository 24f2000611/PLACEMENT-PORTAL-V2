<template>
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>

  <div class="container">
    <div class="row justify-content-center vh-100 align-items-center justify-content-center d-flex ">
      <div class="col-md-5 card p-3 shadow">
        <h2 class="text-center mb-4">Student Registration</h2>

        <div class="mb-3">
          <label class="form-label">Name</label>
          <input type="text" v-model="registerDetails.username" class="form-control">
        </div>

        <div class="mb-3">
          <label class="form-label">Email</label>
          <input type="email" v-model="registerDetails.email" class="form-control">
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" v-model="registerDetails.password" class="form-control">
        </div>

        <button @click="RegisterStudent" class="btn btn-success w-100">Register</button>
        
        <p class="mt-3 text-center">
          Already a user? <router-link to="/login">Login here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>


<script>
export default{  
    data(){
        return {
            "registerDetails":{username:'',password:'',email:''},
            "message":'',
            "messageType":'',
        }
    },
    methods :{
        async RegisterStudent(){
            if(!this.registerDetails.username || !this.registerDetails.password || !this.registerDetails.email){
                this.message = "Credentials cannot be empty";
                this.messageType = 'danger';
                return;
            }
            const payload= {
                username : this.registerDetails.username,
                password : this.registerDetails.password,
                email : this.registerDetails.email,
            };
            try{
                const response = await  fetch('http://localhost:5000/api/student/register',{
                    method : 'POST',
                    headers : {"Content-Type":"application/json"},
                    body :JSON.stringify(payload),
                }); 
                const data = await response.json();
                if(response.ok){
                    this.message = "Student Registration completed";
                    this.messageType ="success",
                    setTimeout(()=>{this.$router.push('/login')},2000)
                }else{
                  this.message=data.message;
                  this.messageType='danger'
                }
            }catch(error){
                this.message= data.message,
                this.messageType = 'danger'
            }  
         } 
    },
    
}


</script>