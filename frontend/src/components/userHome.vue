<template>
    <div>

        <userNavbar />  
        <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
        <button class="btn btn-outline-success" type="submit" @click.prevent="search">Search</button>
        </form> 
     

   
    <div>
    <div class="container">
        <div class="row">
            <div class="col-md-4">
                <div class="card mb-4 border-left-success">
                    <ul>
                        <li v-for="(s , index) in dashData" :key="index">
                            <div class="card-header">
                                <h4 class="card-title">Section: {{ s.section }}</h4>
                            </div>
                            <div class="card-body">
                                <ul>
                                    <li v-for="(i, iIndex) in s.books" :key="iIndex">
                                        <div >
                                            <strong>Id:</strong> {{ i[0] }}
                                        </div>
                                        <div>
                                            <strong>Name:</strong> {{ i[1] }}
                                        </div>
                                        <div>
                                            <strong>Content:</strong> {{ i[2] }}
                                        </div>
                                        <div>
                                            <strong>Author:</strong> {{ i[3] }}
                                        </div>
                                        <button @click="toggleFeedback(i[0])" class="circle-button-2">
                                            {{ isOpen(i[0]) ? 'Close' : 'Open' }}  Add Feedback 
                                        </button>
                                        <feedbackForm v-if="isOpen(i[0])" @form-submitted="feedbackFormSubmission" :iD="iD" />


                                        <button @click="requestBook(i)" class="circle-button">
                                            Request Book 
                                        </button> 
                                    </li>    
                                </ul>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="col-md-4">
                <ul>
                    <li v-for="(s , index) in dashData" :key="index">
                        <strong>User Feedback:</strong>
                        <ul>
                            <li v-for="(i, iIndex) in s.books" :key="iIndex">
                                <div class="feedback-section">
                                    Book Id {{i[0]}}  
                                    <ul>
                                    <li v-for="(feedback, feedbackIndex) in i[4]" :key="feedbackIndex">  
                                    <!-- Display each feedback item -->
                                    {{ feedback.feed }}
                                    <br/>
                                    {{ feedback.username }}
                                    </li>
                                    </ul>
                                </div> 
                            </li>
                        </ul>            
                    </li>   
                </ul>    

            </div>
        </div>
    </div>
</div>  
</div>
  
</template>

<script>
import axios from 'axios';
import userNavbar from "./userNavbar.vue"
import feedbackForm from "./feedbackForm.vue"




export default
{
    name: "userHome",
    components: {userNavbar, feedbackForm} ,
    
    data()
    {
        return { dashData: {    } ,
        searchQuery: '', 
        openFeedbacks: [],
        iD: 0,


    }
      

    },

    methods: 
    {
        async fetchUserApi()
        {
           // const authToken = localStorage.getItem('authToken');


    let result = await axios.get('http://127.0.0.1:5000/user/dashboard/home', {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem("authToken")}`,
    },
  })
  let data = await result.data;
  console.log(data);
  this.dashData = data;
  console.log(this.dashData);

        },

        async search() {

try {

    const response = await axios.get(`http://127.0.0.1:5000/user/dashboard/home/search/${this.searchQuery}`, 
    {headers:{"Content-Type":"application/json",
'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
});
    const data = await response.data;
    console.log(data);
    this.dashData = data;
} catch (error) {
    console.error(error);
    this.fetchUserApi();
}
},  
toggleFeedback(id) 
        {
            const index = this.openFeedbacks.indexOf(id);
            if (index === -1) {
                this.openFeedbacks.push(id);
                
            } else {
                this.openFeedbacks.pop(index, 1);
                this.iD = 0;
            
            }
            this.iD = this.openFeedbacks[0];
            console.log(this.iD)
      
        },
        isOpen(id) 
        {

            return this.openFeedbacks.includes(id);
        },
        feedbackFormSubmission(formData) 
        {
        this.submittedFormData = formData;
        console.log(formData)
        this.fetchUserApi();
        },
    
        async requestBook(book) {
        try {
        const bookId = book[0];
        const response = await fetch(`http://127.0.0.1:5000/user/dashboard/home/request/${bookId}`, {
            method: "POST", 
            headers: 
            {
                "Content-Type":"application/json",
                'Authorization': `Bearer ${localStorage.getItem("authToken")}`,
            
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const request_data = await response.json();
        console.log(request_data);
        window.alert("Request successful");

        } 
        catch (error) {
        console.error('Fetch error:', error);
        }
        
        
    } 
}, 
    mounted()
  {
    this.fetchUserApi();
      
        

    }
        
 
}
</script>

<style scoped>
.container {
  padding: 20px;
}

.card {
  border-radius: 10px;
}

.card-header {
  background-color: #28a745;
  color: #fff;
  padding: 10px;
}

.card-title {
  margin-bottom: 0;
}

.card-body {
  padding: 15px;
}

.book-info {
  margin-bottom: 10px;
}

.book-info strong {
  margin-right: 5px;
}
.feedback-section {
        border: 2px solid #080808;
        padding: 20px;
        margin-bottom: 10px;
        border-radius: 8px;
        margin-left: 20px; 
    }
    .circle-button-2 {
      background-color: lightskyblue; 
      border: none; 
      color: white; 
      padding: 10px 20px; 
      text-align: center; 
      border-radius: 50%;
      text-decoration: none; 
      display: inline-block; 
      font-size: 10px; 
      margin: 4px 2px;
      cursor: pointer; 
      border-radius: 4px; 
    }
    .circle-button {
      background-color: #dcc176; 
      border: none; 
      color: white; 
      padding: 10px 20px; 
      text-align: center; 
      border-radius: 50%;
      text-decoration: none; 
      display: inline-block; 
      font-size: 16px; 
      margin: 4px 2px; 
      cursor: pointer; 
      border-radius: 4px; 
    }    
</style>