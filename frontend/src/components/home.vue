<template>
    <div>

        <adminNavbar /> 
        <form class="d-flex" @submit.prevent="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
        <button class="btn btn-outline-success" type="submit" >Search</button>
        </form>  
    
    <div>
    <div class="container">
        <div class="row">
            <div class="col-md-4">
                    <ul>
                        <li v-for="(s , index) in dashData" :key="index">
                            <div class = "container section-card">
                                <div class="card-header">
                                    <h4 class="card-title">Section: {{ s.section }}</h4>
                                    <h4 class="card-title">Description: {{ s.description }}</h4>
                                    <div class="card-body" >
                                    <div name= "" id="{s.id}">
                                        <button class="circle-button-2"  @click="toggleSection(s.id)">
                                            {{ isOpen(s.id) ? 'Close' : 'Open' }} Add Book
                                        <br/>
                                        
                                        </button>
                                        <bookForm v-if="isOpen(s.id)" @form-submitted="bookFormSubmission" :iD="iD" />
                                       
                                        
                                    </div>
                                    <ul>
                                        <li v-for="(i, iIndex) in s.books" :key="iIndex">
                                            <div class="book-card">
                                            <div>
                                                <strong>Name:</strong> {{ i[0] }}
                                            </div>
                                            <div>
                                                <strong>Content:</strong> {{ i[1] }}
                                            </div>
                                            <div>
                                                <strong>Author:</strong> {{ i[2] }}
                                            </div>
                                            <button @click="toggleBook(i[3])" class="button-update-book">
                                            {{ isBookOpen(i[3]) ? 'Close' : 'Open' }}  Edit Book 
                                            </button>
                                            <bookForm v-if="isBookOpen(i[3])" @form-submitted="editBookFormSubmission" :biD="biD"  :editBookFlag="editBookFlag"/>
                                            <button @click="bookDelete(i)"  class="button-delete-book">  DELETE BOOK </button>
                                            </div>    
                                        </li>
                                    </ul>
                                </div>
                                </div>
                                
                            </div>
                            <button @click="togglEditSection(s.id)" class="button-update-section">  
                                {{ isEditOpen(s.id) ? 'Close' : 'Open' }} Edit Section 
                            </button>
                            <sectionForm v-if="isEditOpen(s.id)" @form-submitted="editSectionFormSubmission" :iD="iD" :editSectionFlag="editSectionFlag" />

                            <button @click="sectionDelete(s)" class="button-delete-section"> Delete Section</button>
                        </li>
                    <br />
                    </ul>
                    <button class="circle-button" @click="showForm">Add Section</button>
                    <sectionForm  v-if="showFormFlag" @form-submitted="sectionFormSubmission"/>
            </div>
            <div class="col-md-4">
                <ul>
                    <li v-for="(s , index) in dashData" :key="index">
                        <strong>User Feedback:</strong>
                        <ul>
                            <li v-for="(i, iIndex) in s.books" :key="iIndex">
                                <div class="feedback-section">
                                    Book {{i[0]}}  
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
import adminNavbar from "./adminNavbar.vue"
import sectionForm from "./sectionForm.vue"
import bookForm from "./bookForm.vue"
//import MyStore from "../store/store";


// import { ref } from 'vue';
// import { getCookie } from 'vue-cookie';

export default
{
    name: "adminHome",
    components: {adminNavbar , sectionForm , bookForm} ,
    // setup() {
    //   const store = MyStore();
    //   return { store };
    // },
   
    // setup() {
    // const store = userStore();
    // return { store };
    // },
    data()
    {
        return { dashData: {} ,showFormFlag: false,
      submittedFormData: null, showBookFormFlag: false,
    //   formData: {
    //     inputData: '' // Initialize form data properties}
        
    //   }
    openSections: [],
    openBooks: [],
    editSections:[],
 
  
      iD: 0,
      biD: 0,
      editSectionFlag: false,
      editBookFlag: false,
      searchQuery: ' '

    
    }
      

    },
   
    
    methods: 
    {
        async fetchData()
        {
            let result = await axios.get('http://127.0.0.1:5000/admin_dashboard/home', {
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
        })
        let data = result.data;
        console.log(data);
        this.dashData = data;
        console.log(this.dashData);


        },
        async search() {

            try {

                const response = await axios.get(`http://localhost:5000/admin_dashboard/home/search/${this.searchQuery}`, 
                {headers:{"Content-Type":"application/json",
                'Authorization': `Bearer ${localStorage.getItem("authToken")}`
        },
            });
                const data = await response.data;
                console.log(data)
                if(data.length > 0 )
                {
                    console.log(data);
                    this.dashData = data;

                }
                else
                {
                    this.fetchData();
                }
               
            } catch (error) {
                this.fetchData();
                
            }
            },




        toggleSection(id) 
        {
            const index = this.openSections.indexOf(id);
            if (index === -1) {
                // Add sectionId to openSections if not present
                this.openSections.push(id);
                
            } else {
                // Remove sectionId from openSections if present
                this.openSections.pop(index, 1);
                this.iD = 0;
            
            }
            this.iD = this.openSections[0];
            console.log(this.iD)
      
        },

        togglEditSection(id) 
        {
            const index = this.editSections.indexOf(id);
            if (index === -1) {
                // Add sectionId to openSections if not present
                this.editSections.push(id);
                this.editSectionFlag = true
            } else {
                // Remove sectionId from openSections if present
                this.editSections.pop(index, 1);
                this.iD = 0;
                this.editSectionFlag = false
            }
            this.iD = this.editSections[0];
            console.log(this.iD)
      
        },

        toggleBook(id) 
        {
            const index = this.openBooks.indexOf(id);
            if (index === -1) {
                // Add sectionId to openSections if not present
                this.openBooks.push(id);
                this.editBookFlag = true

            } else {
                // Remove sectionId from openSections if present
                this.openBooks.pop(index, 1);
                this.biD = 0;
                this.editBookFlag = false;

            
            }
            this.showBookFormFlag=!this.showBookFormFlag;
            this.biD = this.openBooks[0];
            console.log(this.biD)
      
        },

        showForm()
        {
                
            this.showFormFlag = !this.showFormFlag;

        },


        showBookForm()
        { 

        // Check if the sectionId is present in openSections
        //   return this.openSections.includes(id);
        },
        edtBookFlag()
        {
            this.editBookFlag = !(this.editBookFlag);
            return this.editBookFlag;
        },

        edtSectionFlag()
        {
            this.editSectionFlag = !(this.editSectionFlag);
            return this.editSectionFlag;
        },


        isOpen(id) 
        {

            return this.openSections.includes(id);
        },

        isEditOpen(id) 
        {

            return this.editSections.includes(id);
        },

        isBookOpen(id) 
        {

            return this.openBooks.includes(id);
        },


        sectionFormSubmission(formData) 
        {
        // Handle the submitted form data in the main component
        this.submittedFormData = formData;
        console.log(formData)
        this.showFormFlag = false;
        this.fetchData()
        },


        bookFormSubmission(formBookData) 
        {
        // Handle the submitted form data in the main component
        this.submittedBookFormData = formBookData;
        console.log(formBookData)
        alert("new book added")
        //this.showBookFormFlag = false;
        this.fetchData()
        },

        editBookFormSubmission(formBookData) 
        {
        // Handle the submitted form data in the main component
        this.submittedBookFormData = formBookData;
        console.log(formBookData)
        this.editBookFlag = false
        alert("book updated successfully")
        //this.showBookFormFlag = false;
        this.fetchData()
        },

        editSectionFormSubmission(formData) 
        {
        // Handle the submitted form data in the main component
        this.submittedFormData = formData;
        console.log(formData)
        this.editSectionFlag = false
        alert("section updated successfully")
        //this.showBookFormFlag = false;
        this.fetchData()
        },


        async sectionDelete(sd_obj)
        {
                try{
                let id = sd_obj.id
                let sd = await fetch(`http://127.0.0.1:5000/admin_dashboard/home/delete_section/${id}`,
                {
                    method:"DELETE" , headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`}
                })
                if(!sd.ok)
                {
                    throw new Error(`HTTP error! Status: ${sd.status}`);

                }
                let msg = await sd.json();
                console.log(msg);
                window.alert("section is deleted")
                this.fetchData()

            }
            catch(error)
            {
                console.log(error)

            }
       },
       async bookDelete(bd_obj)
        {
                try{
                let id = bd_obj[3]
                let bd = await fetch(`http://127.0.0.1:5000/admin_dashboard/home/delete_book/${id}`,
                {
                    method:"DELETE" , headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`}
                })
                if(!bd.ok)
                {
                    throw new Error(`HTTP error! Status: ${bd.status}`);

                }
                else{
                let msg = await bd.json();
                console.log(msg);
                window.alert("Book is deleted")
                this.fetchData()
                }
            }
            catch(error)
            {
                console.log(error)
                alert(error)

            }
       }
   },
   
   mounted()
   {
    this.fetchData()
   },
}

</script>
<style scoped>
.section-card {
  border: 2px solid #0a0a0a;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
}

.book-card {
  border: 2px solid #080808;
  padding: 20px;
  margin-bottom: 10px;
  border-radius: 8px;
}

.button-delete-book{
      background-color: #e45256;
      border: none; 
      color: white; 
      padding: 10px 20px; 
      text-align: center; 
      border-radius: 50%;
      text-decoration: none; 
      display: inline-block; 
      font-size: 8px; 
      cursor: pointer; 
      border-radius: 4px; 
    }
    .button-update-book{
      background-color: #29e3b5; 
      border: none; 
      color: white; 
      padding: 10px 20px; 
      text-align: center; 
      border-radius: 50%;
      text-decoration: none; 
      display: inline-block; 
      font-size: 8px; 
      cursor: pointer; 
      border-radius: 4px; 
    }
    .button-update-section{
      background-color: #29e3b5;
      border: none; 
      color: white; 
      padding: 10px 20px; 
      text-align: center; 
      border-radius: 50%;
      text-decoration: none; 
      display: inline-block; 
      font-size: 12px; 
      cursor: pointer; 
      border-radius: 4px; 
    }    

    .button-delete-section{
      background-color: #e45256; 
      border: none; 
      color: white; 
      padding: 10px 20px; 
      text-align: center; 
      border-radius: 50%;
      text-decoration: none; 
      display: inline-block; 
      font-size: 12px; 
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
    .feedback-section {
        border: 2px solid #080808;
        padding: 20px;
        margin-bottom: 10px;
        border-radius: 8px;
        margin-left: 20px; 
    }
</style>