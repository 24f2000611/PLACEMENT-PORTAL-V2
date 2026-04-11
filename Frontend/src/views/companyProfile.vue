<template>
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>

      <div class="d-flex justify-content-end align-items-center mb-4 p-2 top-1">
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#postJobModal">
            + New Drive
        </button>
      </div>

<!-- Company details -->

    <div class="container align-items-center justify-content-center mb-5">
      <div class="card shadow p-4 w-100 border-2 position-relative">
        <div class="position-absolute top-0 end-0 p-3">
          <button class="btn btn-sm" @click="ProfileUpdate" :class="editMode ? 'btn-success' : 'btn-primary' ">{{ editMode ? 'Save' :'Edit' }}</button>
        </div>
                    <!-- when not in edit mode -->
        <div v-if="!editMode" class="flex-column d-flex px-4">
          <div class="text-center mb-4"><h2>Company Details</h2></div>
                
                <div class="row mb-3 align-items-center">
                    <div class="col-2 fw-bold h4 text-muted">Name:</div>
                    <div class="col-8 h4">{{ profile.username }}</div>
                </div>

                <div class="row mb-3 align-items-center">
                    <div class="col-2 fw-bold h4 text-muted">Email:</div>
                    <div class="col-8 h4">{{ profile.email }}</div>
                </div>

                <div class="row mb-3 align-items-center">
                    <div class="col-2 fw-bold h4 text-muted">Location:</div>
                    <div class="col-8 h4">{{ profile.location }}</div>
                </div>

                <div class="row mb-3 align-items-center">
                    <div class="col-2 fw-bold h4 text-muted">Industry:</div>
                    <div class="col-8 h4">{{ profile.industry }}</div>
                </div>

                <div class="row mb-3 align-items-center">
                    <div class="col-2 fw-bold h4 text-muted">HR Contact:</div>
                    <div class="col-8 h4">{{ profile.hr_contact }}</div>
                </div>

                <div class="row mb-3 align-items-center">
                    <div class="col-2 fw-bold h4 text-muted">Website:</div>
                    <div class="col-8 h4">{{ profile.website }}</div>
                </div>
            </div>
            <!-- when in edit mode -->
              <div class="flex-column d-flex w-100 text-align-center" v-else>
                <div class="mb-3">
                  <label for="username">Username</label>
                  <input type="text" v-model="profile.username" class="form-control form-control-sm">
                </div>

                <div class="mb-3">
                    <label for="password">Password</label>
                    <input type="password" v-model="profile.password" class="form-control form-control-sm">
                </div>

                <div class="mb-3">
                    <label for="email">Email</label>
                    <input type="email" v-model="profile.email" class="form-control form-control-sm">
                </div>

                <div class="mb-3">
                    <label for="location">location</label>
                    <input type="text" v-model="profile.location" class="form-control form-control-sm">
                </div>

                <div class="mb-3">
                    <label for="industry">Industry</label>
                    <input type="text" v-model="profile.industry" class="form-control form-control-sm">
                </div>

                <div class="mb-3">
                    <label for="hr_contact">HR.Contact</label>
                    <input type="text" v-model="profile.hr_contact" class="form-control form-control-sm">
                </div>

                <div class="mb-3">
                    <label for="website">Website</label>
                    <input type="text" v-model="profile.website" class="form-control form-control-sm">
                </div>
              </div>
    </div>
  </div>
    
    
    <!-- Modal for posting the drive -->
    

  <div class="container mt-4">

    <div class="modal fade" id="postJobModal" tabindex="-1" aria-labelledby="postJobModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="postJobModalLabel">Post a New Placement Drive</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close" id="closeModalBtn"></button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="post_job">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Job Title</label>
                  <input type="text" class="form-control" v-model="newjob.job_title" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Job Type</label>
                  <select class="form-select" v-model="newjob.type" required>
                    <option value="" disabled>Select Type...</option>
                    <option value="Full-Time">Full-Time</option>
                    <option value="Internship">Internship</option>
                  </select>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Salary / Stipend</label>
                  <input type="text" class="form-control" v-model="newjob.salary" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Location</label>
                  <input type="text" class="form-control" v-model="newjob.location" required>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Eligibility Criteria</label>
                  <input type="text" class="form-control" v-model="newjob.eligibility" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Application Deadline</label>
                  <input type="date" class="form-control" v-model="newjob.app_deadline" required>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Job Description</label>
                <textarea class="form-control" rows="3" v-model="newjob.job_desc" required></textarea>
              </div>

              <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">Submit for Approval</button>
              </div>
            </form>
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
            "newjob":{
                "job_title":'',
                "job_desc":'',
                "eligibility":'',
                "type":'',
                "salary":'',
                "app_deadline":''
            },
            "profile":{
              "username":'',
              "location":'',
              "password":'',
              "email":'',
              "hr_contact":'',
              "industry":'',
              "website":''
            },
            editMode:false,
            message :'',
            messageType:''
        }
    },
    async mounted(){
      const response = await fetch('http://localhost:5000/api/company/profile',{
        method:"GET",
        headers:{'Authentication-Token':localStorage.getItem('token')}
      });
      if (response.ok){
        const data = await response.json()
        this.profile =data.profile
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
            const res = await fetch('http://localhost:5000/api/company/profile/update',{
              method:"POST",
              headers:{
                "Content-Type":"application/json",
                "Authentication-Token":localStorage.getItem('token')
              },
              body :JSON.stringify(this.profile)
            })
            if(res.ok){
                    this.editMode=false,
                    this.message="Profile Updated Successfully",
                    this.messageType="success"

                }
          }catch(error){
                this.message="Profile cannot be updated",
                this.messageType="danger"
            }
        },
            async post_job(){
            try{
                const response = await fetch('http://localhost:5000/api/company/profile/post-job',{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    },
                    body:JSON.stringify(this.newjob) // post drive 
                })
                const data =await response.json()
                if(response.ok){
                    this.message="Drive posted successfully,it will be visible after admin's approval"
                    this.messageType='success'
                    document.getElementById('closeModalBtn')?.click();
                    this.clearForm()

                }
                else{
                    this.message=data.message || 'cannot post drive'
                    this.messageType = 'danger'
                    document.getElementById('closeModalBtn')?.click();

                }
            }catch(error){
                this.message='Failed to post drive'
                this.messageType='danger'
                document.getElementById('closeModalBtn').click();
            }
        },
        clearForm(){
            this.newjob={
                job_title:'',
                job_desc:'',
                eligibility:'',
                location:'',
                salary:'',
                type:'',
                app_deadline:''
            };
        },
        
    },

}





</script>