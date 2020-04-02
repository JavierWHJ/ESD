$(document).ready(pageReady());
function pageReady(){
    const queryString = window.location.search;
    const searchvalue = queryString.substring(1,queryString.length);
    if(searchvalue || searchvalue.length != 0){
        var serviceURL = 'http://localhost:8000/api/v1/doctor/'+ searchvalue;
        console.log(serviceURL);
        $(async() => {
            try {
                const response = await fetch(
                    serviceURL,
                    {method: "GET"}
                );
                var doctor = await response.json();
                var count = Object.keys(doctor).length;
                if(count == 1){
                    var doctorr = doctor.doctors;
                    var data = "";
        
                    doctorr.forEach(function(d){
                        data += `
                                <div class="card">
                                <div class="card-body">
                                    <div class="doctor-widget">
                                        <div class="doc-info-left">
                                            <div class="doctor-img">
                                                <a href="doctor-profile.html?doctorID=${d.doctorID}&docName=${d.name}">
                                                    <img src="assets\\img\\doctors\\${d.name}.jpg" class="img-fluid" alt="User Image">
                                                </a>
                                            </div>
                                            <div class="doc-info-cont">
                                                <h4 class="doc-name"><a href="doctor-profile.html?doctorID=${d.doctorID}&docName=${d.name}"> ${d.name} </h4>
                                                <p class="doctorID">${d.doctorID}</p>
                                                <div class="rating">
                                                    <i class="fas fa-star filled"></i>
                                                    <i class="fas fa-star filled"></i>
                                                    <i class="fas fa-star filled"></i>
                                                    <i class="fas fa-star filled"></i>
                                                    <i class="fas fa-star"></i>
                                                </div>
                                                <div class="clinic-details">
                                                    <p class="doc-location"><i class="fas fa-map-marker-alt"></i> Singapore ${d.postalcode}</p>
                                                    <p class="doc-contact">+65 ${d.phone}</p>
                                                </div>
                                                <div class="clinic-services">
                                                    <span>${d.services}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="doc-info-right">
                                            <div class="clini-infos">
                                                <ul>
                                                    <li><i class="far fa-money-bill-alt"></i> $ ${d.price} </li>
                                                    <li><a href="#0" onclick="onHtmlClick(${d.postalcode})" class="btn_listing">View on Map</a></li>
                                                </ul>
                                            </div>
                                            <div class="clinic-booking">
                                                <a class="view-pro-btn" href="doctor-profile.html?doctorID=${d.doctorID}&docName=${d.name}">View Profile</a>
                                                <a class="apt-btn" href="booking.html?doctorID=${d.doctorID}&docName=${d.name}">Book Appointment</a>
                                                <br>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                                `;
                    })
                    var element = document.getElementsByClassName('col-lg-7')[0]
                    element.innerHTML += data;
                } else{
                    var data = "";
                    data = `
                                <div class="card">
                                <div class="card-body">
                                    <div class="doctor-widget">
                                        <div class="doc-info-left">
                                            <div class="doctor-img">
                                                <a href="doctor-profile.html?doctorID=${doctor.doctorID}&docName=${doctor.name}">
                                                    <img src="assets\\img\\doctors\\${doctor.name}.jpg" class="img-fluid" alt="User Image">
                                                </a>
                                            </div>
                                            <div class="doc-info-cont">
                                                <h4 class="doc-name"><a href="doctor-profile.html?doctorID=${doctor.doctorID}&docName=${doctor.name}"> ${doctor.name} </h4>
                                                <p class="doctorID">${doctor.doctorID}</p>
                                                <div class="rating">
                                                    <i class="fas fa-star filled"></i>
                                                    <i class="fas fa-star filled"></i>
                                                    <i class="fas fa-star filled"></i>
                                                    <i class="fas fa-star filled"></i>
                                                    <i class="fas fa-star"></i>
                                                </div>
                                                <div class="clinic-details">
                                                    <p class="doc-location"><i class="fas fa-map-marker-alt"></i> Singapore ${doctor.postalcode}</p>
                                                    <p class="doc-contact">+65 ${doctor.phone}</p>
                                                </div>
                                                <div class="clinic-services">
                                                    <span>${doctor.services}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="doc-info-right">
                                            <div class="clini-infos">
                                                <ul>
                                                    <li><i class="far fa-money-bill-alt"></i> $ ${doctor.price} </li>
                                                    <li><a href="#0" onclick="onHtmlClick(${doctor.postalcode})" class="btn_listing">View on Map</a></li>
                                                </ul>
                                            </div>
                                            <div class="clinic-booking">
                                                <a class="view-pro-btn" href="doctor-profile.html?doctorID=${doctor.doctorID}&docName=${doctor.name}">View Profile</a>
                                                <a class="apt-btn" href="booking.html?doctorID=${doctor.doctorID}&docName=${doctor.name}">Book Appointment</a>
                                                <br>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                                `;
                    var element = document.getElementsByClassName('col-lg-7')[0]
                    element.innerHTML += data;
                }
            } catch (e){
                console.log(e);
            }
        });
    }else{
        var serviceURL = "http://localhost:8000/api/v1/doctor";
        $(async() => {
            try {
                const response = await fetch(
                    serviceURL,
                    {method: "GET"}
                );
                var doctors = await response.json();
                var doctors = doctors.doctors;
                var data = "";
    
                doctors.forEach(function(doctor){
                    data += `
                            <div class="card">
                            <div class="card-body">
                                <div class="doctor-widget">
                                    <div class="doc-info-left">
                                        <div class="doctor-img">
                                            <a href="doctor-profile.html?doctorID=${doctor.doctorID}&docName=${doctor.name}">
                                                <img src="assets\\img\\doctors\\${doctor.name}.jpg" class="img-fluid" alt="User Image">
                                            </a>
                                        </div>
                                        <div class="doc-info-cont">
                                            <h4 class="doc-name"><a href="doctor-profile.html?doctorID=${doctor.doctorID}&docName=${doctor.name}"> ${doctor.name} </h4>
                                            <p class="doctorID">${doctor.doctorID}</p>
                                            <div class="rating">
                                                <i class="fas fa-star filled"></i>
                                                <i class="fas fa-star filled"></i>
                                                <i class="fas fa-star filled"></i>
                                                <i class="fas fa-star filled"></i>
                                                <i class="fas fa-star"></i>
                                            </div>
                                            <div class="clinic-details">
                                                <p class="doc-location"><i class="fas fa-map-marker-alt"></i> Singapore ${doctor.postalcode}</p>
                                                <p class="doc-contact">+65 ${doctor.phone}</p>
                                            </div>
                                            <div class="clinic-services">
                                                <span>${doctor.services}</span>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="doc-info-right">
                                        <div class="clini-infos">
                                            <ul>
                                                <li><i class="far fa-money-bill-alt"></i> $ ${doctor.price} </li>
                                                <li><a href="#0" onclick="onHtmlClick(${doctor.postalcode})" class="btn_listing">View on Map</a></li>
                                            </ul>
                                        </div>
                                        <div class="clinic-booking">
                                            <a class="view-pro-btn" href="doctor-profile.html?doctorID=${doctor.doctorID}&docName=${doctor.name}">View Profile</a>
                                            <a class="apt-btn" href="booking.html?doctorID=${doctor.doctorID}&docName=${doctor.name}">Book Appointment</a>
                                            <br>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                            `;
                })
                var element = document.getElementsByClassName('col-lg-7')[0]
                element.innerHTML += data;
            }
            catch (e) {
                console.log(e);
                alert("Failed");
            }
        });
    }
}