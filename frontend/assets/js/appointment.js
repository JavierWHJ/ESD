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
                alert(message)
            }
            
            $(async() => {
                serviceURL = 'http://localhost:8000/api/v1/start_booking';
                try{
                    const response =
                    await fetch(
                        serviceURL,
                        {
                            method: "POST",
                            headers: {"Content-Type" : "application/json"},
                            mode: 'no-cors',
                            body: JSON.stringify({
                                bookingID: bid,
                                status: "started",
                                location: pos
                            })
                        })
                }catch (error){
                    showError('h');
                }finally{
                    window.location.reload();
                }
            });
        }
    })
}
