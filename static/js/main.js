// main.js
function processSelection() {
    // Get the selected values
    var selectedCandlePattern = document.getElementById('candlePattern').value;
    var selectedSector = document.getElementById('sector').value;
  
    // Example: Log the selected values (you can replace this with your desired logic)
    console.log('Selected Candle Pattern:', selectedCandlePattern);
    console.log('Selected Sector:', selectedSector);
    
    data = {
        "selectedCandlePattern" : selectedCandlePattern,
        "selectedSector" : selectedSector
    }
    console.log(data)
    fetch('/process_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Process the result from Python
       document.getElementById('showing-results').innerHTML = "<p>" + data.result + "</p>";

    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    
    
    //displayResult(selectedCandlePattern,selectedSector)
    // Call additional functions or perform actions based on the selected values
    // ...
  }
  


  function displayResult(selectedCandlePattern,selectedSector){

    var resultContainer = document.getElementById('showing-results')
    resultContainer.innerHTML = `<h2> ${selectedCandlePattern} ${selectedSector} <h2>`

  }