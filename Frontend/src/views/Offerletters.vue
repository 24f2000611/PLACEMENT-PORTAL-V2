<template>
    <div v-if="message" :class="['alert', 'text-bg-' + messageType,'alert-dismissible', 'fade', 'show','toast'] " role="alert">
        {{ message }}
        <button type="button" class="btn-close" @click="message = ''"></button>
    </div>


    <h2 class="text-center">My Offers</h2>
        <div class="row d-flex gap-3 justify-content-center">
            <div class="students col-md-5 mb-2" v-for="offer in offers" :key="offer.id">
                <div class="col-12">
                    <div class="card">
                        <h5 class="card-header bg-info">🎫{{ offer.username }}</h5>
                        <div class="card-body row gap-3 p-2">
                            <span class="card-text col-5 ">Name : {{ offer.company_name }}</span>
                            <span class="card-text col-4 ">🎯Title : {{ offer.job_title }}</span>
                            <span class="card-text col-4 ">💸Package: {{ offer.package_offered }}</span>
                            <span class="card-text col-4 ">📍Location :{{ offer.location}}</span>
                            <span class="card-text col-5 ">📑Website : {{ offer.website}}</span>
                            <span class="card-text col-5 ">📑HR Contact{{ offer.hr_contact}}</span>
                            <span class="card-text col-5 ">📋Joining Date: {{ offer.joining_date}}</span>
                            <span class="card-text col-5 ">⏱️Interview Date :{{ offer.interview_date}}</span>
                            <span class="card-text col-5 ">📑Offer Description: {{ offer.description}}</span>
                            <span class="card-text col-5 ">Job Description :{{ offer.job_desc}}</span>
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
            "offers":[],
            "message":"",
            "messageType":""
        }
    },
    methods:{
        async dash(){
            try{
                const res = await fetch('http://localhost:5000/api/student/offer-letters',{
                    method:"GET",
                    headers:{
                        "Content-Type":"application/json",
                        "Authentication-Token":localStorage.getItem('token')
                    }
                });
                const data = await res.json();
                if(res.ok){
                    this.offers = data.offers;
                }else{
                    this.message=data.message,
                    this.messageType='danger'
                }

            }catch(error){
                this.message="Could not get offer letters",
                this.messageType='danger'
            }
        }
    },
    mounted(){
        this.dash();
    }
}

</script>