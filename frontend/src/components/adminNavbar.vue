<template>
    <div>
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
        <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <router-link :to="{ name: 'adminHome' }" class="nav-link">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{ name: 'adminAccess' }" class = "nav-link"> Access</router-link>
              </li>
              <li class="nav-item">
                <router-link :to="{ name: 'adminSummary' }" class = "nav-link"> Summary</router-link>
              </li>
              <li class="nav-item" @click="logout" style="cursor: pointer;"  >
                logout
              </li>
        </ul>
        </div>
      </nav>
      <h1> Dashboard </h1>
      <router-view/>
    </div>  
  
</template> 
  
<script>


export default 
{
  name: 'adminNavbar',
  methods: 
  {
    async logout()
    {

      let llog = await fetch('http://127.0.0.1:5000/logout', {
            method: "GET", 
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`}},);
      if (llog.ok)
        {
          let data = await llog.json
          console.log(data)
          localStorage.setItem('authToken', data.access_token);
          this.$router.push({ name: 'LoginForm' });

        } 
         
      
    }
  }
  
  

};
</script>


<style scoped>
.nav-link {
padding: 0 1rem;
margin-right: 5rem;
}


</style>