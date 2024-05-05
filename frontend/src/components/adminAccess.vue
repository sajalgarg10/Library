<template>
<div>
<adminNavbar />
  <div>
    <div>
      <h2>Issued Books</h2>
      <div class="row">
        <ul>
          <li v-for="(issue, index) in accessData.issued" :key="index" class="col-md-4">
            <div @click="revokeapi(issue)" class="tt">
                book id: {{issue.book_id}} book name: {{ issue.book_name }} issued to {{ issue.user_name }}  id: {{ issue.user_id }}
              </div>
          </li>
        </ul>
        </div>
      </div>
    </div>
    <div>
    <h2>Requested Books</h2>
    <div class="row">
      <ul>
        <li v-for="(request, index) in accessData.request" :key="index" class="col-md-4">
          <div class="tt">
            
              book id: {{ request.book_id }} book name: {{ request.book_name }} requested by {{ request.user_name }} id: {{ request.user_id }}
              <button @click="requestapi(request)" class="button-update" > Accept</button>
              <button @click="declineapi(request)"  class="button-delete">Deline</button>

          </div>
        </li>
      </ul>
    </div>
    </div>
    <div>
      <h2>Returned Books</h2>
      <div class="row">
        <ul>
        <li v-for="(returned, index) in accessData.return" :key="index" class="col-md-4">
            <div @click="returnapi(returned)" class="tt" >
              book_id : {{ returned.book_id}} book name : {{ returned.book_name }} returned by {{ returned.user_name }} id: {{ returned.user_id }}
            </div>
        </li>
      </ul>
    </div>  
    </div>


</div>
    
</template>



<script>

//import axios from 'axios';
import axios from "axios";
import adminNavbar from "./adminNavbar.vue"

export default {
  name: 'adminAcess',
  data(){
    return{
      accessData :{},
    }
  },
  components: {adminNavbar}, 
  methods: {
    async fetchAccessApi()
    {
      let result = await axios.get('http://127.0.0.1:5000/admin_dashboard/access', {
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
        })
        
          //let data = await result.json;
          //console.log(data);
          console.log(result.data)
          this.accessData = result.data;
          console.log(this.accessData)
   


    },
    async requestapi(i)
    {
      try{
      let id = i.user_id
      let requ = await fetch(`http://127.0.0.1:5000/admin_dashboard/access/grant/${id}`, {  
            method : "POST",
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
        });
        if(!requ.ok)
        {
          let msg = await requ.json();
            throw new Error(`HTTP error! Status: ${requ.status}  message:${msg.message}`);
        }
          let redata = await requ.json();
          console.log(redata)
          window.alert("request successfully granted")
          this.fetchAccessApi();


    }
    catch (error) 
      {
        console.error('Fetch error:', error);
        alert(error)
        this.fetchAccessApi();
      }
    },  

    async declineapi(i)
    {
      try{
      let id = i.user_id
      let requ_decline = await fetch(`http://127.0.0.1:5000/admin_dashboard/access/decline/${id}`, {  
            method : "POST",
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
        });
        if(!requ_decline.ok)
        {
          let msg = await requ_decline.json();
            throw new Error(`HTTP error! Status: ${requ_decline.status} message: ${msg.message}`);
        }
          let redata_decline = await requ_decline.json();
          console.log(redata_decline)
          window.alert("request successfully revoked")
          this.fetchAccessApi();


    }
    catch (error) 
      {
        console.error('Fetch error:', error);
      }
    },  

    async revokeapi(i)
    {
      try{
      let id = i.user_id;
      let rev = await fetch(`http://127.0.0.1:5000/admin_dashboard/access/revoke/${id}`, {  
            method : "POST",
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
        });
        if(!rev.ok)
        {
          throw new Error(`HTTP error! Status: ${rev.status}`);

        }
          let revdata = await rev.json();
          console.log(revdata)
          window.alert("access successfully revoked")
          this.fetchAccessApi();
    }
  catch(error){
    console.error('Fetch error:', error);


  }
},
async returnapi(i)
    {
      try{
      let id = i.user_id;
      let retu = await fetch(`http://127.0.0.1:5000/admin_dashboard/access/return/${id}`, {  
            method : "POST",
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
        });
        if(!retu.ok)
        {
          throw new Error(`HTTP error! Status: ${retu.status}`);

        }
          let retudata = await retu.json();
          console.log(retudata)
          window.alert("return successful ")
          this.fetchAccessApi();
    }
  catch(error){
    console.error('Fetch error:', error);


  }
},
  }, 
  mounted()
  {
    this.fetchAccessApi();
  }

  
  

};

</script>


<style scoped>

.tt {
  margin: 10px;
  padding: 10px;
  border: 1px solid #ccc;
}



ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  cursor: pointer;
}

li:hover {
  background-color: #f0f0f0;
}
.button-update{
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
    .button-delete{
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
</style>
