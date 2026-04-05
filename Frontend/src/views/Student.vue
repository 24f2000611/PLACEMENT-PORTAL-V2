<template>
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>

    <h2 class="text-center">Active Drives</h2>
        <div class="row d-flex gap-3 justify-content-center">
            <div class="students col-md-5 mb-2" v-for="drive in active_drives" :key="drive.drive_id">
                <div class="col-12">
                    <div class="card">
                        <h5 class="card-header bg-info">🎫{{ drive.job_title }}</h5>
                        <div class="card-body row gap-2">
                            <span class="card-text col-4">🎯{{ drive.type }}</span>
                            <span class="card-text col-4">💸{{ drive.salary }}</span>
                            <span class="card-text col-4">📍{{ drive.location}}</span>
                            <span class="card-text col-4">⏱️{{ drive.app_deadline}}</span>
                            <span class="card-text col-4">📋{{ drive.eligibility}}</span>
                            <span class="card-text col-12">📑{{ drive.job_description}}</span>
                        </div>
                        <button @click="applyJob(drive.drive_id)" class="btn btn-outline-primary btn-sm col-md-2 m-2">Apply</button>
                    </div>
                </div>
            </div>
        </div>
    
    <h2 class="text-center">My Applications</h2>
        <div class="row gap-3 d-flex justify-content-center gap-3">
            <div class="applications col-md-5 mb-3" v-for="app in applications" :key="app.app_id">
                <div class="col-12">
                    <div class="card">
                        <h5 class="card-header bg-info">🎫{{ app.job_title }}</h5>
                        <div class="card-body row gap-2">
                            <span class="card-text col-4">🎯{{ app.type }}</span>
                            <span class="card-text col-4">💸{{ app.salary }}</span>
                            <span class="card-text col-4">📍{{ app.location}}</span>
                            <span class="card-text col-4">⏱️{{ app.app_deadline}}</span>
                            <span class="card-text col-8">📋{{ app.eligibility}}</span>
                            <span class="card-text col-12">📑{{ app.description}}</span>
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
            "search_query":'',
            "active_drives":[],
            "applications":[],
            "message":'',
            "messageType":''
        }
    },
    methods:{
        async Dash(){
            try{
                const response = await fetch('http://localhost:5000/api/student',{
                    "method":"GET",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    }
            });
            const data = await response.json();
            if(response.ok){
                this.active_drives = data.active_drives,
                this.applications=data.applications
            }    
        }catch(error){
                this.message="Error laoding the dashboard",
                this.messageType= "danger"
            }
        },
        async applyJob(id){
            try{
                const res = await fetch("http://localhost:5000/api/student/applyjob",{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    },
                    body:JSON.stringify({drive_id:id}),
                });
                const data = await res.json();
                if(res.ok){
                    this.message=data.message || "Application Applied Successfully";
                    this.messageType="success";
                    this.Dash();
                }else{
                    this.message=data.message || "Cannot apply";
                    this.messageType='danger';
                }
            }catch(error){
                this.message='Application failed';
                this.messageType='danger';
            }
        }
    },
    mounted(){
        this.Dash();
    }
}

</script>


<style scoped>
body{
    background-color: rgb(58, 96, 248);
}
</style>