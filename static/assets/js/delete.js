
   document.getElementById("detailsForm").addEventListener("submit", function() {
       var currentDate = new Date().toISOString().split('T')[0]; // Get current date in 'YYYY-MM-DD' format
       document.getElementById("current_date").value = currentDate; // Set value of hidden field to current date
   });