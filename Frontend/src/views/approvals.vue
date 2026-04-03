<template>
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>

    <div class="container mt-4">
        <h2 class="mb-4">Pending Companies</h2>
        <div class="card shadow-sm mb-4" v-for="comp in pending_comp" :key="comp.id">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h4 class="card-title mb-0">{{ comp.username }}</h4>
                    <button :class="getButtonClass(comp.approve_status)" @click="handleApprovals(comp.id,'Company')">
                        {{ comp.approve_status }}
                    </button>
                </div>

                <div class="row">
                    <div class="col-md-4 mb-2">
                        <strong>Email:</strong> <p class="mb-0">{{ comp.email }}</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <strong>Industry:</strong> <p class="mb-0">{{ comp.industry }}</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <strong>Location:</strong> <p class="mb-0">{{ comp.location }}</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <strong>HR Contact:</strong> <p class="mb-0">{{ comp.hr_contact }}</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <strong>Website:</strong> <p class="mb-0">{{ comp.website }}</p>
                    </div>
                </div>
            </div>
        </div>
    <div v-if="pending_comp.length==0">No Pending Companies</div>


        <h3 class="mt-5 mb-3">Pending Drives</h3>
        <div v-if="pending_drives.length>0">
        <div class="card shadow-sm mb-4" v-for="drive in pending_drives" :key="drive.id">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h4 class="card-title mb-0">{{ drive.job_title }}</h4>
                    <button :class="getButtonClass(drive.approve_status)" @click="handleApprovals(drive.id,'Drive')">
                        {{ drive.approve_status }}
                    </button>
                </div>

                <div class="row">
                    <div class="col-md-4 mb-2">
                        <strong>Company:</strong> <p class="mb-0">{{ drive.company_name }}</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <strong>Eligibility:</strong> <p class="mb-0">{{ drive.eligibility }}</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <strong>Salary:</strong> <p class="mb-0">{{ drive.salary }}</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <strong>Job Type:</strong> <p class="mb-0">{{ drive.type }}</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <strong>Industry:</strong> <p class="mb-0">{{ drive.industry }}</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <strong>Location:</strong> <p class="mb-0">{{ drive.location }}</p>
                    </div>
                    <div class="col-md-12 mt-2 text-danger">
                        <strong>Deadline:</strong> {{ drive.app_deadline }}
                    </div>
                </div>
            </div>
        </div>
        </div>
        <div v-else>No pending drives</div>
    </div>
</template>


<script>

export default{
    data(){
        return{
                "pending_comp":[],
                "pending_drives":[],
                "message":'',
                "messageType":''
        }
    },
    methods:{
        getButtonClass(status){
            if(status==='Pending') return 'btn btn-warning';
            if(status==='Rejected') return 'btn btn-danger';
            return 'btn btn-success';
        },
        async fetchApprovals(){
            const response = await fetch('http://localhost:5000/api/admin/approvals',{
            method:"GET",
            headers:{
                "Authentication-Token":localStorage.getItem('token'),
            }
        });
        const data = await response.json();
        this.pending_comp = data.pending_comp;
        this.pending_drives = data.pending_drives;
            
        },
        async handleApprovals(id,type){
        const response =  await fetch('http://localhost:5000/api/admin/approvals',{
            method:"POST",
            headers:{
                "Authentication-Token":localStorage.getItem('token'),
                "Content-Type":"application/json"
            },
            body:JSON.stringify({ "id":id,"type":type})
        });
        const data = await response.json();
        if(response.ok){
            this.message = "Status updated";
            this.messageType='success';
            this.fetchApprovals();
            }
        }
    },
    
    mounted(){
            this.fetchApprovals();
    }
}   


</script>