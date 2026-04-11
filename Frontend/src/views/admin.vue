<script>
export default{
    data(){
        return{
            "search_query":'',
            "reg_students":[],
            "reg_companies":[],
            "active_drives":[],
            "applications":[],
            "searchResults": { students: [], companies: [], drives: [], applications: [] },
            "query":'',
            "isSearching":false,
            "dashboard_info":{TotalCompanies:0,TotalStudents:0,TotalDrives:0,TotalApplications:0},
            "message":'',
            "messageType":''
        }
    },
    computed:{
        noResults(){
            if(!this.searchResults) return true;    
            return Object.values(this.searchResults).every(arr=>arr.length===0);
        }
    },
    methods:{
        async Dashboard(){
            try{
                const response =await fetch('http://localhost:5000/api/admin',{
                    method:"GET",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token'),
                    }
                });
                const data = await response.json();
                if(response.ok){
                    this.reg_companies = data.reg_companies;
                    this.reg_students = data.reg_students;
                    this.active_drives =data.drives;
                    this.applications =data.applications;
                    this.dashboard_info = data.dashboard_info;
                }
            }catch(error){
                this.message="Error Loading Dashboard";
                this.messageType="danger";
            }
        },
        async handleDelete(id,type){
            try{
                const response = await fetch('http://localhost:5000/api/admin/delete',{
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    },
                    body:JSON.stringify({"id":id,"type":type})
                });
                const data = await response.json()
                if(response.ok){
                    this.message=data.message;
                    this.messageType='success';
                    this.Dashboard();
                    if(this.isSearching) this.search();

                }else{

                    this.message=data.message;
                    this.messageType='danger'
                }
            }catch(error){
                this.message="Delete failed:Server Error",
                this.messageType='danger'
            }
        },

        async search(){
            console.log("Starting search result ",this.query);
              if(!this.query){
                    this.isSearching=false;
                    return;
                }
            try{
                console.log("sending request to backend")
                const response = await fetch("http://localhost:5000/api/admin/search",{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authentication-Token":localStorage.getItem('token')
                },
                body: JSON.stringify({"query":this.query}),
            });
            const data = await response.json()
            console.log("backend data",data)
            if(response.ok){
                this.searchResults=data.results || { students: [], companies: [], drives: [], applications: [] };
                this.isSearching=true;
                console.log("4. isSearching is now:", this.isSearching);
            }else{
                this.message=data.message,
                this.messageType='danger'
            }
        }catch(error){
            console.error("SEARCH ERROR:", error);
            this.message='Error fetching result data',
            this.messageType='danger'
        }
        }
  
    },

    watch:{
        '$route.query.q':{
            immediate:true,
            handler(newVal){
                console.log("URL Watcher triggered! New URL Query:", newVal);
                if(newVal){
                    this.query = newVal;
                    this.search();
                }else{
                    this.query='';
                    this.isSearching=false;
                };
            }
        }
    },
    mounted(){
        this.Dashboard();
    }
}
  
            
</script>

<template>
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>

<div class="container">
    <div class="stats row gap-4 p-2">
        <div class="col-md-2 info">
            <span>Total Students:{{ dashboard_info.TotalStudents }}</span>
        </div>
         <div class="col-md-2 info">
            <span>Total Companies:{{ dashboard_info.TotalCompanies }}</span>
        </div>
         <div class="col-md-2 info">
            <span>Total Drives:{{ dashboard_info.TotalDrives }}</span>
        </div>

         <div class="col-md-2 info">
            <span>Total Applications:{{ dashboard_info.TotalApplications }}</span>
        </div>
    
    </div>
    <div v-if="isSearching">

        <div v-if="searchResults.students && searchResults.students.length>0">
            <h2>Results for Students</h2>
            <div class="col-6">
                <div class="card">
                    <div class="card-body row" v-for="student in searchResults.students" :key="student.id">
                        <h5 class="card-header">{{ student.username }}</h5>
                        <span class="card-text col-4">📧 {{ student.email }}</span>
                        <span class="card-text col-4">🎓{{ student.education }}</span>
                        <span class="card-text col-4">⚡{{ student.skill}}</span>
                        <span class="card-text col-4">📑{{ student.description}}</span>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="searchResults.companies && searchResults.companies.length>0">
            <h2>Results for companies</h2>
            <div class="col-6">
                <div class="card">
                    <div class="card-body row" v-for="company in searchResults.companies" :key="company.company_id">
                        <div class="card-header">
                            <span class="badge text-bg-warning position-absolute end-0 px-1 mx-3">{{ company.approve_status }}</span>
                            <h5>{{ company.username }}</h5>
                        </div>
                        <span class="card-text col-4">📧{{ company.email }}</span>
                        <span class="card-text col-4">📞{{ company.hr_contact }}</span>
                        <span class="card-text col-4">🌐{{ company.website}}</span>
                        <span class="card-text col-4">📍{{ company.location}}</span>
                        <span class="card-text col-4">🏭{{ company.industry}}</span>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="searchResults.drives && searchResults.drives.length>0">
            <h2>Results for Drives</h2>
            <div class="col-6">
                <div class="card">
                    <div class="card-body row" v-for="drive in searchResults.drives" :key="drive.id">
                        <div class="card-header">
                            <span class="badge text-bg-primary position-absolute top-0 px-1 m-3 end-0">{{ drive.post_status }}</span>
                                <h5> 🎫{{ drive.job_title }}</h5>
                            </div>
                            <span class="card-text col-4">📋{{ drive.eligibility }}</span>
                            <span class="card-text col-4">📍{{ drive.location }}</span>
                            <span class="card-text col-4">🎯{{ drive.type}}</span>
                            <span class="card-text col-4">⌛{{ drive.app_deadline}}</span>
                            <span class="card-text col-4">📑{{ drive.description }}</span>
                        </div>
                </div>
            </div>
        </div>

       <div v-if="searchResults.applications && searchResults.applications.length>0">
            <h2>Results for Applications</h2>
            <div class="col-6">
                <div class="card">
                    <div class="card-body row" v-for="app in searchResults.applications" :key="app.application_id">
                        <h5 class="card-header">🎫{{ app.job_title }}</h5>
                        <span class="card-text col-4">🧑‍🎓{{ app.student_name }}</span>
                        <span class="card-text col-4">🏢{{ app.company_name }}</span>
                        <span class="card-text col-4">📍{{ app.location}}</span>
                        <span class="card-text col-4">💸{{ app.salary}}</span>
                        <span class="card-text col-4">🎯{{ app.type}}</span>
                        <span class="card-text col-4">⏱️{{ app.date_applied}}</span>
                        <span class="card-text col-4">📑{{ app.description}}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <!-- registerd students -->
        <h2 class="text-center">Registered Students</h2> 
        <div class="row d-flex gap-3">
            <div class="students col-md-5" v-for="student in reg_students" :key="student.id">
                <div class="col-12">
                    <div class="card">
                        <h5 class="card-header bg-info">{{ student.username }}</h5>
                        <div class="card-body row gap-2">
                            <span class="card-text col-4">📧 {{ student.email }}</span>
                            <span class="card-text col-6">⚡{{ student.skill}}</span>
                            <span class="card-text col-4">🎓{{ student.education }}</span>
                            <span class="card-text col-6">📑{{ student.description}}</span>

                            <div class="col-md-2 position-absolute end-0 bottom-0 p-3 mx-2">
                                <span><button class="btn btn-danger" @click="handleDelete(student.id,'Student')">Delete</button></span>
                            </div>
                        </div>              
                    </div>
                </div>
            </div>
        </div>
  
        <!-- registered companies -->
        <h2 class="text-center">Registered Companies</h2>
        <div class="row">
            <div class="companies col-md-6" v-for="company in reg_companies" :key="company.company_id">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header bg-info">
                            <span class="badge text-bg-primary position-absolute end-0 px-1 mx-3">{{ company.approve_status }}</span>
                            <h5>{{ company.username }}</h5>
                        </div>
                        <div class="card-body row gap-3">
                            <span class="card-text col-4 ">📧{{ company.email }}</span>
                            <span class="card-text col-6 ">📞{{ company.hr_contact }}</span>
                            <span class="card-text col-6 ">🏭{{ company.industry}}</span>
                            <span class="card-text col-4 ">🌐{{ company.website}}</span>
                            <span class="card-text col-6 ">📍{{ company.location}}</span>
                            <div class="col-md-2 end-0 bottom-0 position-absolute p-3">
                                <span><button class="btn btn-danger" @click="handleDelete(company.company_id,'Company')">Delete</button></span>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- active drives -->
        <h2 class="text-center">Active Drives</h2>
        <div class="row">
            <div class="Drives col-md-6" v-for="drive in active_drives" :key="drive.drive_id">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header bg-info">
                            <span class="badge text-bg-primary position-absolute top-0 px-1 m-3 end-0">{{ drive.post_status }}</span>
                            <h5> 🎫{{ drive.job_title }}</h5>
                        </div>
                        <div class="card-body row gap-3">
                            <span class="card-text col-3">📋{{ drive.eligibility }}</span>
                            <span class="card-text col-3">📍{{ drive.location }}</span>
                            <span class="card-text col-3">🎯{{ drive.type}}</span>
                            <span class="card-text col-3">⌛{{ drive.app_deadline}}</span>
                            <span class="card-text col-6">📑{{ drive.description }}</span>

                            <div class="col-md-2 end-0 bottom-0 postion-absolute p-3">
                                <span><button class="btn btn-danger" @click="handleDelete(drive.drive_id,'Drive')">Delete</button></span>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- active application -->
        <h2 class="text-center">Applications</h2>
        <div class="row">
            <div class="Applications col-md-5" v-for="app in applications" :key="app.application_id">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header bg-info">
                            <span class="badge text-bg-primary position-absolute top-0 px-1 m-3 end-0">{{ app.app_status }}</span>
                            <h5> 🎫{{ app.job_title }}</h5>
                        </div>
                        <div class="card-body  row gap-3">
                            <span class="card-text col-3">🧑‍🎓{{ app.student_name }}</span>
                            <span class="card-text col-3">🏢{{ app.company_name }}</span>
                            <span class="card-text col-3">📍{{ app.location}}</span>
                            <span class="card-text col-4">💸{{ app.salary}}</span>
                            <span class="card-text col-4">🎯{{ app.type}}</span>
                            <span class="card-text col-4">⏱️{{ app.date_applied}}</span>
                            <span class="card-text col-8">📑{{ app.description}}</span>
                            <div class="col-md-2 end-0 bottom-0 position-absolute mx-4 p-2">
                                <span><button class="btn btn-danger end-0" @click="handleDelete(app.application_id,'Application')">Delete</button></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</template>




<style scoped>
.info{
    background-color: lightblue;
    color: black;
    border-radius: 12px;
}


</style>