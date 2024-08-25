let formEle = document.getElementById('downloadForm');

formEle.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the default way
    
    const formData = new FormData(this);
    
    fetch('http://127.0.0.1:8000/download', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('status').innerText = data.status;
    })
    .catch(error => {
        document.getElementById('status').innerText = 'An error occurred: ' + error;
    });
});
