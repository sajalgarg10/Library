<template>
    <div>
        <form @submit.prevent="submitBookForm" class="book-form">
        <!-- Your form inputs go here -->
        <label for="inputData">Name:</label>
        <input v-model="formBookData.name" type="text" id="name" required>
        <br />
        <label for="inputData">Content:</label>
        <input v-model="formBookData.content" type="text" id="content" required>
        <br />
        <label for="inputData">Author:</label>
        <input v-model="formBookData.author" type="text" id="author" required>
        <label for="inputData">Book:</label>
        <input v-model="formBookData.book" type="text" id="book" required>
        <br />

        <!-- Submit button inside the form component -->
        <button type="submit">Submit</button>
        </form>
        <p>{{ iD }}</p>
        
    </div>
  </template>
  
  <script>
  //import MyStore from "../store/store";

 
  
  export default {
    name: "bookForm",
    props: {
    iD: Number,
    biD: Number,
    editBookFlag: Boolean
  },
    data() {
      return {
     // Controls the visibility of the modal
        formBookData: {
        name: '',
        content: '',
        author: '',
        book:' '
      },
      };
      
    },
    methods: 
    {
        async submitBookForm() 
       {  
        try{
        if(this.editBookFlag)
        {
          const resp = await fetch(`http://127.0.0.1:5000/admin_dashboard/home/update_book/${this.biD}`, {
            method: "PUT", 
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
            body: JSON.stringify({
                name: this.formBookData.name,
                content: this.formBookData.content,
                author: this.formBookData.author,
                book: this.formBookData.book,

            }),
          });

          if (resp.ok)
          {
            console.log(resp)
            const data = await resp.json();
            console.log(data)
            this.$emit('form-submitted', this.formBookData, this.editBookFlag);
          }


        }
        else{
            const resp = await fetch(`http://127.0.0.1:5000/admin_dashboard/home/add_book/${this.iD}`, {
            method: "POST", 
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
            body: JSON.stringify({
                name: this.formBookData.name,
                content: this.formBookData.content,
                author: this.formBookData.author,
                book: this.formBookData.book,

            }),
          });

          if (resp.ok)
          {
            console.log(resp)
            const data = await resp.json();
            console.log(data)
            this.$emit('form-submitted', this.formBookData);
          }
        }
       } 
      catch(error)
      {
        console.log(error)
        alert(error)
      } 
    }  
   }
}
</script>
<style scoped>
.book-form {
  max-width: 300px; 
  margin: auto; 
}

.book-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}


.book-form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  box-sizing: border-box;
}


.book-form button {
  background-color: #007bff;
  color: #fff;
  padding: 10px;
  border: none;
  cursor: pointer;
}


.book-form button:hover {
  background-color: #0056b3;
}
</style>  