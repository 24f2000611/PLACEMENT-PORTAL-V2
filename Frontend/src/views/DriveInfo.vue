<template>
        <div v-if="message" :class="['alert', 'text-bg-' + messageType, 'alert-dismissible', 'fade', 'show','toast']" role="alert">
            {{ message }}
            <button type="button" class="btn-close" @click="message = ''"></button>
        </div>
<div class="container">
    <div class="card my-4 col-12">
        <div class="card-header bg-primary text-white"><h2>{{ drive_det.job_title }}</h2></div>
        <div class="card-body row">
            <h4 class="card-text col-md-3">Location : {{ drive_det.location }}</h4> 
            <h4 class="card-text col-md-3">Salary: {{ drive_det.salary }}</h4> 
            <h4 class="card-text col-md-3">Eligibility: {{ drive_det.eligibility }}</h4> 
            <h4 class="card-text col-md-3">Type : {{ drive_det.type }}</h4> 
            <h4 class="card-text col-md-6">Deadline: {{ drive_det.app_deadline }}</h4> 
            <h4 class="card-text col-md-6">Job Desc : {{ drive_det.job_desc }}</h4> 
        </div>
    </div>

    <div class="row">
        <div class="col-md-6" v-for="student in stu_appli" :key="student.id">
        <div class="col-12">
            <div class="card">
                <span class="card-header bg-info">Name: {{ student.username }}</span>
                <div class="card-body row gap-3">
                    <span class="card-text col-4">Email: {{ student.email }}</span>
                    <span class="card-text col-4">Skills: {{ student.skill }}</span>
                    <span class="card-text col-4">Education: {{ student.education }}</span>
                    <span class="card-text col-6">description: {{ student.description }}</span>
                    
                    <div class="col-md-2 end-0 bottom-0 position-absolute">
                        <span><button class="btn btn-primary" @click="AppStatus(student.app_id)">{{ student.status }}</button></span>
                    </div>
                </div>
            </div>
        </div>
        </div>
    </div>
</div>

</template>

<script>
export default{
    data(){
        return{
            "stu_appli":[],
            "drive_det":{job_title:'',job_desc:'',eligibility:'',app_deadline:'',location:'',type:'',salary:'',post_status:'',date_applied:''},
            "message":'',
            "messageType":''
        }
    },
    methods:{
        async ShowApps(){
            const driveId = this.$route.params.id;
            try{
                const response = await fetch(`http://localhost:5000/api/company/drive/info/${driveId}`,{
                    method:"GET",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    }
                });
                const data =await response.json();
                if(response.ok){
                    this.stu_appli =data.stu_appli;
                    this.drive_det = data.drive_det;
                    // this.message="Applications Retrieved";
                    // this.messageType='success';
                }else{
                    this.message="Could not find applications";
                    this.messageType='danger';
                }
            }catch(error){
                this.message="Error No application Found.";
                this.messageType='danger';
            }
        },
        async AppStatus(id){
            try{
                const response = await fetch("http://localhost:5000/api/company/drive/info/status",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":localStorage.getItem('token')
                },
                body:JSON.stringify({"id":id}),
            });
            const data = await response.json();
            if(response.ok){
                this.message=data.message;
                this.messageType='success'
                this.ShowApps();
            }else{
                this.message = data.message;
                this.messageType='danger'
            }
            }catch(error){
                this.message="Could not update application status",
                this.messageType='danger'
            }
    },

    },
    mounted(){
        this.ShowApps();
    }
}

</script>

