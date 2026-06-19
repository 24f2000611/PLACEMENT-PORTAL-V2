<template>
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>
<div class="container align-items-center justify-content-center vh-50 d-flex p-5">
    <div class="box border  border-2 p-4 position-relative">
        <div class="position-absolute top-0 end-0 p-3">
            <button class="btn btn-sm" @click="ProfileUpdate" :class="editMode ? 'btn-success' : 'btn-primary' ">{{ editMode ? 'Save' :'Edit' }}</button>
        </div>
        <div v-if="!editMode" class="flex-column d-flex w-100"> 
            <div class="text-center"><h2>Student Details</h2></div>
            <h4 class="mb-5">Username:  {{ profile.username }}</h4>
            <h4 class="mb-5">Email:  {{ profile.email }}</h4>
            <h4 class="mb-5">Education:  {{ profile.education }}</h4>
            <h4 class="mb-5">Skills:  {{ profile.skill }}</h4>
            <h4 class="mb-5">Description:  {{ profile.description }}</h4>
        </div>   

        <div v-else class="flex-column d-flex w-50 text-align-center">
            <div class="mb-2">
                <label for="username">Username</label>
                <input type="text" v-model="profile.username" class="form-control form-control-sm">
            </div>

            <div class="mb-2">
                <label for="password">Password</label>
                <input type="password" v-model="profile.password" class="form-control form-control-sm">
            </div>

            <div class="mb-2">
                <label for="email">Email</label>
                <input type="email" v-model="profile.email" class="form-control form-control-sm">
            </div>

            <div class="mb-2">
                <label for="education">Education</label>
                <input type="text" v-model="profile.education" class="form-control form-control-sm">
            </div>

            <div class="mb-2">
                <label for="skill">Skill</label>
                <input type="text" v-model="profile.skill" class="form-control form-control-sm">
            </div>

            <div class="mb-2">
                <label for="description">Description</label>
                <input type="text" v-model="profile.description" class="form-control form-control-sm">
            </div>
        </div>
    </div>
</div>


</template>


<script>
export default{
    data(){
        return{
        editMode:false,
        profile: {
            "username" : '',
            "password":'',
            "education" : '',
            "email" : '',
            "skill" : '',
            "description" : '',
            "message":'',
            "messageType":''
            }
        }
    },
    async mounted(){
        const response = await fetch('/api/student/profile',{
            headers:{
                'Authentication-Token':localStorage.getItem('token'),
            }
        });
        if(response.ok){
            const data = await response.json();
            this.profile=data.profile;
        }
     
    },
    methods:{
        ProfileUpdate(){
            if(this.editMode){
                this.saveProfile();
            }
            else{
                this.editMode=true
            }
        },
        async saveProfile(){
            try{
                const response = await fetch('/api/student/profile/update',{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    },
                    body:JSON.stringify(this.profile)

                });
                if(response.ok){
                    this.editMode=false,
                    this.message="Profile Updated Successfully",
                    this.messageType="success"

                }
            }catch(error){
                this.message="Profile cannot be updated",
                this.messageType="danger"
            }
        }
    }
   
}


</script>

<style scoped>

.box{
    border:2px solid black;
    height: 500px;
    width:900px;
    position: relative;
    display: flex;
    border-radius: 20px;
    background-color: lightblue;

}

</style>