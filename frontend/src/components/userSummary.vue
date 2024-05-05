<template>
    <div>
        <userNavbar/>
        <div>
        <apexchart type="bar" :options="chartOptions" :series="series" height="350" />
        </div>
    </div>    
</template>



<script>
import userNavbar from "./userNavbar.vue";
import axios from "axios";
import VueApexCharts from 'vue3-apexcharts';



export default
{
    name: "userSummary",
    components: {userNavbar , apexchart:  VueApexCharts } ,
    data() {
  return {
    chartOptions: {
      chart: {
        id: 'summaryChart',
      },
      title: {
        text: 'Summary till today',
        align: 'center',
        style: {
          fontSize: '20px',
          fontFamily: 'cursive',
        },
      },
      legend: {
        position: 'top',
        horizontalAlign: 'center',
        offsetY: -10,
      },
      xaxis: {
        categories: [], 
        labels: {
          offsetY: -2,
          style: {
            fontSize: '10px',
          },
        },
        title: {
          text: 'Name of Books',
          style: {
            fontSize: '15px',
            fontWeight: 'bold',
          },
        },
      },
      yaxis: {
        title: {
          text: '# Number Of Feedback',
          style: {
            fontSize: '15px',
            fontWeight: 'bold',
          },
        },
      },
    },
    series: [
      {
        name: 'Feedback Chart',
        data: [],
      },
    ],
  };
},
    methods:
    {
        async summaryAPI()
        {
            try{
            let result = await axios.get('http://127.0.0.1:5000/user/dashboard/summary', {
            headers:{"Content-Type":"application/json",
            'Authorization': `Bearer ${localStorage.getItem("authToken")}`},
        })
        let data = result.data;
        let book_data  = data[0];
        //console.log(book_data)
        let feedback_data = data[2];
        //this.xaxis.books = [];
        for(let i = 0; i < book_data.length; i++)
        {
          this.chartOptions.xaxis.categories.push(book_data[i]);

        }
        console.log(this.chartOptions.xaxis.categories)
    // Update series data
      this.series[0].data = feedback_data;


      }
            catch(error)
            {
                console.log(error)
            }
        },

    }, 
    mounted()
    {
        this.summaryAPI();
    }  



}
</script>
