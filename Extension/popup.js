function getPrediction(url) {
    fetch('http://127.0.0.1:5000/', {
        method: 'POST',
        body: new URLSearchParams({ 'url': url }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Check if 'state' property exists in data
        if (data.hasOwnProperty('state')) {
            // Update the popup UI based on the prediction result
            if (data.state === 0) {
                document.getElementById('result').textContent = 'Legitimate';
            } else {
                document.getElementById('result').textContent = 'Phishing';
            }
        } else {
            console.error('Error: Invalid response from server');
        }
    })
    .catch(error => console.error('Error:', error));
}

function addEventListenerForOnOffButton() {
    var checkbox = document.getElementById("OnOffButton");
    if (checkbox !== null) {
        checkbox.addEventListener('click', function() {
            var cb = document.getElementById('switch');
            chrome.storage.local.set({'state': cb.checked}, function() {});
            console.log("switch 1 ", cb.checked);
            
            // Call getPrediction when the toggle button is clicked
            getPrediction('http://127.0.0.1:5000/'); // Replace 'https://www.example.com' with the actual URL
        });
    }
}
