// main.js
function processSelection() {




    // Get the selected values
    var selectedCandlePattern = document.getElementById('candlePattern').value;
    var selectedSector = document.getElementById('sector').value;

    var showingResults = document.getElementById('showing-results');

    showingResults.style.display = 'block';

    var spinnerContainer = document.getElementById('spinnerContainer');
    spinnerContainer.style.display = 'block';
  
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

        spinnerContainer.style.display = 'none';

       var resultHtml = '<ul>';

       // Iterate through the list and create list items
       data.result.forEach(item => {
           resultHtml += '<li>' + item + '</li>';
       });

       resultHtml += '</ul>';

       // Update the content of the showing-results section
       document.getElementById('showing-results').innerHTML += resultHtml;

    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    
    
  }
  


  function displayResult(selectedCandlePattern,selectedSector){

    var resultContainer = document.getElementById('showing-results')
    resultContainer.innerHTML = `<h2> ${selectedCandlePattern} ${selectedSector} <h2>`

  }