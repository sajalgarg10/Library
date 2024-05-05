<template>
    <div>
        <form @submit.prevent="submitForm" class="section-form">
        <!-- Your form inputs go here -->
        <label for="inputData">Name:</label>
        <input v-model="formData.name" type="text" id="name" required>
        <br />
        <label for="inputData">Description:</label>
        <input v-model="formData.description" type="text" id="description" required>
        <br />

        <!-- Submit button inside the form component -->
        <button type="submit">Submit</button>
        </form>
        
    </div>
  </template>
  
  <script>
  //import MyStore from "../store/store";

 
  
  export default {
    name: "sectionForm",
    props: {
    iD: Number,
    editSectionFlag: Boolean

  },
    data() {
      return {
        formData: {
        name: '',
        description: ''
      },
      };
    },

    methods: 
    {
        async submitForm() 
     
       {
        try{
          if(this.editSectionFlag)
          {
            const resp = await fetch(`http://127.0.0.1:5000/admin_dashboard/home/update_section/${this.iD}`, {
            method: "PUT", 
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
            body: JSON.stringify({
                name: this.formData.name,
                description: this.formData.description
            }),
          });

          if (resp.ok)
          {
            console.log(resp)
            const data = await resp.json();
            console.log(data)
            this.$emit('form-submitted', this.formData, this.editSectionFlag);
          }


          }
          else{
            const resp = await fetch('http://127.0.0.1:5000/admin_dashboard/home/add_section', {
            method: "POST", 
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
            body: JSON.stringify({
                name: this.formData.name,
                description: this.formData.description
            }),
          });

          if (resp.ok)
          {
            console.log(resp)
            const data = await resp.json();
            console.log(data)
            this.$emit('form-submitted', this.formData);
          }
        }
      }
      catch(error)
      {
        console.log(error)
        alert(error);
      }
       }    
   }
}
  </script>

<style scoped>
.section-form {
  max-width: 300px; 
  margin: auto; 
}


.section-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}


.section-form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  box-sizing: border-box;
}


.section-form button {
  background-color: #28a745; 
  color: #fff;
  padding: 10px;
  border: none;
  cursor: pointer;
}


.section-form button:hover {
  background-color: #218838; 
}
</style>  