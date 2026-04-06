<template>
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>

    <h2 class="text-center">My Applications</h2>
        <div class="row gap-3 d-flex justify-content-center gap-3">
            <div class="applications col-md-5 mb-3" v-for="app in applications" :key="app.app_id">
                <div class="col-12">
                    <div class="card">
                        <span class="badge rounded-pill bg-danger top-0 end-0 m-2 position-absolute">{{ app.status }}</span>
                        <h5 class="card-header bg-info">🎫{{ app.job_title }}</h5>
                        <div class="card-body row gap-2">
                            <span class="card-text col-3">{{ app.company_name }}</span>
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
            "applications":[],
            "message":'',
            "messageType":''
        }
    },
    methods:{
        async appli(){
            try{
                const response = await fetch('http://localhost:5000/api/student',{
                    method:"GET",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    }
                });
                const data = await response.json();
                console.log(data);
                if(response.ok){
                    this.applications=data.applications;
                }else{
                    this.message = data.message;
                    this.messageType= data.messageType;
                }
            }catch(error){
                this.message="Could not fetch application history";
                this.messageType='danger';

            }
        },
    },
    
    mounted(){
        this.appli();
    }
}

</script>