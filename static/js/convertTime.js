function convertTime() {
    const timeString = document.getElementById("total-time").textContent;
    console.log(timeString);
    const minutes = getTimeInMinutes(timeString);
    document.getElementById("total-time").textContent = `${minutes}min`;
  }
  
  function getTimeInMinutes(timeString) {
    var minutesString = timeString.slice(2, -1);
    console.log(minutesString);

    var minutes = parseInt(minutesString, 10);
  
    return minutes;
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    convertTime();
  });