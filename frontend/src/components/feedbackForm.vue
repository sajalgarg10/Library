<template>
    <div>
        <form @submit.prevent="submitFeedbackForm" class="feedback-form">
        <!-- Your form inputs go here -->
        <label for="inputData">Feedback:</label>
        <input v-model="formfeedbackData.feed" type="text" id="feed" required>

        <!-- Submit button inside the form component -->
        <button type="submit">Submit</button>
        </form>
        <p>{{ iD }}</p>
        
    </div>
  </template>
  
  <script>
  //import MyStore from "../store/store";

 
  
  export default {
    name: "feedbackForm",
    props: {
    iD: Number,
  },
    data() {
      return {
     // Controls the visibility of the modal
        formfeedbackData: {
        feed: '',
      },
      };
      
    },

    methods: 
    {
        async submitFeedbackForm()
        
        { 
      try
       {  
          const resp = await fetch(`http://127.0.0.1:5000/user/dashboard/home/feedback/${this.iD}`, {
            method: "POST", 
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
            body: JSON.stringify({
                feed: this.formfeedbackData.feed,

            }),
          });

          if (resp.ok)
          {
            console.log(resp)
            const data = await resp.json();
            console.log(data)
            this.$emit('form-submitted', this.formfeedbackData);
          }
          else{
            throw new Error(`HTTP error! Status: ${resp.status}`);
          }
       }    
    catch(error)
    {
      console.log(error)
      alert(error)

    }
  },
}
  }
</script>
<style scoped>
.feedback-form {
  max-width: 300px; 
  margin: auto; 
}


.feedback-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}


.feedback-form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  box-sizing: border-box;
}


.feedback-form button {
  background-color: #007bff;
  color: #fff;
  padding: 10px;
  border: none;
  cursor: pointer;
}


.feedback-form button:hover {
  background-color: #0056b3;
}
</style>  