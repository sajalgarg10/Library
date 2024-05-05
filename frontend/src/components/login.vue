<template>
    <div>
        <h1>Welcome Admin</h1>
        <form @submit.prevent="login">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required>
        <br>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required>
        <br>
        <button v-on:click="login">Login</button>
        </form>
         <router-link to="/user"> User login</router-link>
         <br />
         <router-link to="/register"> Register</router-link>
    </div>
</template>

<script>




export default{
    name: 'loginUser',
    data()
    {
      return {
        username:'',
        password:''
      }

    },
      methods: 
      {
        async login() 
        {
        try{
          const resp = await fetch('http://127.0.0.1:5000/', {
            method: "POST", 
            headers:{
              "Content-Type":"application/json"
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password

            }),
          });
          if (resp.ok)
          {
            console.log(resp)
            const data = await resp.json();
            console.log(data)
            localStorage.setItem('authToken', data.access_token);
            this.$router.push({ name: 'adminHome' });

          }
          else{
          let msg = await resp.json();
          throw new Error(`message: ${msg.message}`);
          }

        }
      catch(error)
      {
        alert(error)


      }
    }
      },
}
</script>

<style scoped>


/* styles.css */

body {
  font-family: 'Arial', sans-serif;
}

h1 {
  color: #333;
}

form {
  max-width: 400px;
  margin: 0 auto;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.router-link {
  text-decoration: none;
  color: #3498db;
  margin-right: 10px;
}

.router-link:hover {
  text-decoration: underline;
}


</style>