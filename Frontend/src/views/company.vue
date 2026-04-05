<template>
    <div class="container mt-4">
        <div v-if="message" :class="['alert', 'text-bg-' + messageType, 'alert-dismissible', 'fade', 'show','toast']" role="alert">
            {{ message }}
            <button type="button" class="btn-close" @click="message = ''"></button>
        </div>

        <h2> Manage  Drives</h2>

        <div class="row mt-3">
            <div class="col-md-4 mb-4" v-for="d in drives" :key="d.drive_id">
                <div class="card h-100 shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <span class="badge rounded-pill bg-danger top-0 start-0 position-absolute">{{ d.application_count }}</span>
                        <h5 class="card-title px-4 mb-1"> 🎫 {{ d.job_title }}</h5>
                        <div class="position-absolute top-0 end-0 d-flex m-2">
                            <span class="badge bg-warning text-black">{{ d.post_status }}</span>
                        </div>
                    </div>
                    <div class="card-body"> 
                        <div class="row">
                            <p class="card-text col-12"><strong>📍 Location:</strong> {{ d.location }}</p>
                            <p class="card-text col-6"><strong>💼 Type:</strong> {{ d.type }}</p>
                            <p class="card-text col-6"><strong>💰 Salary:</strong> {{ d.salary }}</p>
                            <p class="card-text col-12"><strong>🎓 Eligibility:</strong> {{ d.eligibility }}</p>
                            <p class="card-text col-12 text-danger"><strong>⏱️ Deadline:</strong> {{ d.app_deadline }}</p>
                        </div>
                    </div>
                    <div class="card-footer d-flex justify-content-between align-items-center">
                  
                        <button class="btn btn-primary" @click="$router.push(`/company/drive/info/${d.drive_id}`)">View</button>
                        <button class="btn btn-primary" @click="deleteDrive(d.drive_id)">Delete</button>
                        <button class="btn btn-primary" @click="driveStatus(d.drive_id)">Toggle</button>

                    </div>
                </div>
            </div>
        </div>
        
        <div v-if="drives.length === 0">
            You haven't posted any drives yet.
        </div>
    </div>
</template>


<script>

export default{
    data(){
        return{
            "drives":[],
            "message":"",
            "messageType":""
        }
    },
    methods:{
        async dash(){
            try{
                const response = await fetch('http://localhost:5000/api/company',{
                    method:"GET",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    }
                });
                const data = await response.json();
                if(response.ok){
                    this.drives = data.drives;
                }
            }catch(error){
                this.message="Error loading the dashboard";
                this.messageType='danger';
            }
        },
        
        async driveStatus(drive_id){
            try{
                const res = await fetch('http://localhost:5000/api/company/drive-status',{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    },
                    body: JSON.stringify({'drive_id':drive_id})

                });
                const data = await res.json();
                if(res.ok){
                    this.message=data.message,
                    this.messageType='success'
                    this.dash()
                }else{
                    this.message=data.message,
                    this.messageType='danger'
                }
            }catch(error){
                this.message="Drive status could not be updated";
                this.messageType='danger'
            }
        },
        async deleteDrive(drive_id){
            try{
                const response = await fetch('http://localhost:5000/api/company/delete',{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    },
                    body: JSON.stringify({'drive_id':drive_id})
                });
                const data = await response.json();
                if(response.ok){
                    this.message=data.message,
                    this.messageType='success',
                    this.dash()
                }else{
                    this.message=data.message;
                    this.messageType='danger';
                }
            }catch(error){
                this.message = data.message,
                this.messageType='danger'
            }
        }
    },
    mounted(){
        this.dash();
    }

}
</script>