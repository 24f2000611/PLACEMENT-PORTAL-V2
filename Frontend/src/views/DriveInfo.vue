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
                    <span class="card-text col-6">Education: {{ student.education }}</span>
                    <span class="card-text col-6">description: {{ student.description }}</span>
                    
                    <div class="col-6 gap-3 editorial end-0 bottom-0 position-absolute m-2 px-5">
                        <span><button class="btn btn-primary" @click="AppStatus(student.app_id)">{{ student.status }}</button></span>
                        <span><button class="btn btn-warning" @click="OpenOfferModal(student)" data-bs-toggle="modal" data-bs-target="#offerModal">Send Offer</button></span>
                    </div>
                </div>
            </div>
        </div>
        </div>
    </div>
</div>

<!-- Modal for sending the job offer -->
<div class="modal fade" id="offerModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header bg-success text-white">
                <h5 class="modal-title">Send Offer to {{ activeOffer.username }}</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="mb-3">
                    <label class="form-label fw-bold">Salary Package</label>
                    <input type="text" class="form-control" v-model="activeOffer.package" placeholder="In LPA">
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Expected Joining Date</label>
                    <input type="date" class="form-control" v-model="activeOffer.joining_date">
                </div>

                 <div class="mb-3">
                    <label class="form-label fw-bold">Interveiw Date</label>
                    <input type="date" class="form-control" v-model="activeOffer.interview_date">
                </div>

                <div class="mb-3">
                    <label class="form-label fw-bold">Additional Message/Remarks</label>
                    <textarea class="form-control" v-model="activeOffer.message" rows="3" placeholder="Welcome to the team!"></textarea>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="button" class="btn btn-success" @click="submitOffer" data-bs-dismiss="modal">Send Offer</button>
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
            "activeOffer":{app_id:null,username:'',package:'',joining_date:'',job_title:'',job_desc:'',interview_date:'',message:''},
            "message":'',
            "messageType":''
        }
    },
    methods:{
        async ShowApps(){
            const driveId = this.$route.params.id;
            try{
                const response = await fetch(`/api/company/drive/info/${driveId}`,{
                    method:"GET",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    }
                });
                const data = await response.json();
                if(response.ok){
                    this.stu_appli =data.stu_appli;
                    this.drive_det = data.drive_det;
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
                const response = await fetch("/api/company/drive/info/status",{
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
        async submitOffer(){
            try{
                const response = await fetch('/api/company/drive/info/offer-letter',{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    },
                    body: JSON.stringify({
                        "app_id":this.activeOffer.app_id,
                        "job_title":this.activeOffer.job_title,
                        "job_desc":this.activeOffer.job_desc,
                        "package":this.activeOffer.package,
                        "message":this.activeOffer.message,
                        "username":this.activeOffer.username,
                        "joining_date":this.activeOffer.joining_date,
                        "interview_date":this.activeOffer.interview_date

                    }),
                });
                const data= await response.json();
                if(response.ok){
                    this.message=data.message;
                    this.messageType='success';
                    this.ShowApps();

                }else{
                    this.message=data.message;
                    this.messageType='danger';
                }
            }catch(error){
                    this.message="Could not send the Offer";
                    this.messageType='danger';
            }
        },
        OpenOfferModal(student){
            this.activeOffer={
                app_id :student.app_id,
                username : student.username,
                package:'',
                joining_date:'',
                message:''
            };
        },
    },
    mounted(){
        this.ShowApps();
    }
}

</script>


<style scoped>
.editorial{
    display: inline-flex;
}
</style>