<template>
    <div>
    <userNavbar />   

    <h1> Issued Books </h1>
    <div>
    <ul>
      <li v-for="(issued, index) in issuedData" :key="index">
        <div>
            {{ issued.book }}
            <div @click="returnapi(issued)">
            Book ID: {{ issued.book_id }}<br>
            Book Name: {{ issued.book_name }}<br>
            User ID: {{ issued.user_id }}<br>
            User Name: {{ issued.user_name }}<br>
            </div>
        </div>
      </li>
    </ul>
  </div>


    </div>
    
</template>


<script>

import axios from "axios"
import userNavbar from "./userNavbar.vue"



export default
{
    name: "userIssuedBook",
    components: {userNavbar} ,
    data()
    {
        return {
            issuedData: []
        }
    },
    methods: {
        async issuedDataApi()
        {
            let result = await axios.get('http://127.0.0.1:5000/user/dashboard/issued', {
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
  });
    let data = result.data;
    console.log(data);
    this.issuedData = data;
    console.log(this.issuedData);    


        },
        async returnapi(i)
        {
            try{
            let id = i.book_id
            const response = await fetch(`http://127.0.0.1:5000/user/dashboard/issued/return/${id}`, {
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

        const return_data = await response.json();
        console.log(return_data);
        window.alert("Return request send successful"); 

            }
            catch(error)
            {
                console.error('Fetch error:', error);

            }
        },

    }, 

    mounted()
    {
        this.issuedDataApi();
        
    }



}
</script>
