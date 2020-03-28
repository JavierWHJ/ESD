var x = document.getElementsByClassName('bg-info-light').length
if (x==0){
    setTimeout(onReady,1000)
}

function onReady(){
    $('.bg-success-light').click(function(){
        console.log('clicked');
        var element = this;
        var bid = this.parentNode.parentNode.querySelector('h5 span.booking').textContent
        getLocation();
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }
        
        function showPosition(position) {
            var pos = {lat:position.coords.latitude, long:position.coords.longitude}
            function showError(message) {
                alert(message);
            }
            if (element.innerText != "Appointment Started"){
                $(async() => {
                    // change url to localhost:8000/api/v1/start_booking
                    // var serviceURL = 'http://localhost:5005/start_booking';
                    serviceURL = 'http://localhost:8000/api/v1/start_booking';
                    try {
                        const response =
                        fetch(
                            serviceURL,
                            {
                                method: "POST",
                                headers: {"Content-Type" : "application/json"},
                                mode: "no-cors",
                                body: JSON.stringify({
                                    bookingID: bid,
                                    status: "started",
                                    location: pos
                                })
                            }
                        );
                        element.innerText = "Appointment Started"
                    } catch (error) {
                        // Errors when calling the service; such as network error, 
                        // service offline, etc
                        showError
                        ('Failed to start appointment, please try again');                
                    } 
                });
            }else{
                console.log("already started")
            }
        }
    })		
}
