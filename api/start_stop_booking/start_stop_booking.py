from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import pika
import requests
app = Flask(__name__)

CORS(app, support_credentials=True)
bookingURL = "http://booking:5000/bookings"
notificationURL = 'http://notification:5000/notifications'
customerURL = "http://customer:5000/customer"

@app.route('/start_booking', methods=['POST'])
@cross_origin(supports_credentials=True)
def start_booking():
    # booking and notification
    # no need entire booking object. bookingid, status, notificationID
    data = request.get_data()
    booking = json.loads(data)
    if "status" not in booking:
        return jsonify({
            "message": "error occurred when starting booking."
        }), 500
        
    r = requests.put(bookingURL, json=booking)
    if r.status_code != 200:
        return jsonify({
            "message": "error occurred when starting booking."
        }), 500
    else:
        try:
            r = r.json()
            customerID = r['customerID']
            doctorID = r['doctorID']
            
            # retrieve doctor's current location
            docLocation = f"{booking['location']['lat']},{booking['location']['long']}" 
            # retrieve customer object
            customer = requests.get(customerURL+'/'+customerID).json()

            # prepare google distance api call
            googleDistMatrixURL = "https://maps.googleapis.com/maps/api/distancematrix/json?"
            params = {
                "key": "AIzaSyChZfWfurzE-Tml80GT8G1hxPO6dblJ41I",
                "origins": docLocation,
                "destinations": customer['postalcode']
            }
            # make the get request 
            distanceResponse = requests.get(googleDistMatrixURL,params=params).json()

            ETA = ""
            try:
                # extract the the estimated time if exist
                ETA = distanceResponse['rows'][0]['elements'][0]['duration']['text']
            except:
                # could not get ETA..
                pass
            
            if ETA == "":
                message = "The doctor is making his/her way to your location."
            else:
                message = f"The doctor is on the way to your location. The estimated arrival time is in {ETA}."

            # no error so send notification to customer
            hostname = "host.docker.internal"  # change to host.docker.internal before building image
            port = 5672  # port of rabbitmq
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
            channel = connection.channel()

            # set up exchange name
            exchangename="notification_topic"
            channel.exchange_declare(exchange=exchangename, exchange_type='topic')

            r = requests.get(notificationURL).json()
            nid = r['notifications'][-1]['nid'] + 1

            notification = {
                "nid" : nid,
                "sender": doctorID,
                "receiver" : customerID,
                "message" : message
            }
            
            notification = json.dumps(notification, default=str)
            channel.basic_publish(exchange=exchangename, routing_key="booking.notification", body=notification, properties=pika.BasicProperties(delivery_mode = 2))
            connection.close()

            return jsonify({
                "message": "Booking started."
            }), 200
        
        except:
            return jsonify({
                "message": "An error occurred when trying to start the appointment. Please try again later."
            }), 500

@app.route('/stop_booking', methods=['POST'])
@cross_origin(supports_credentials=True)
def stop_booking():

    data = request.get_data()
    booking = json.loads(data)
    r = requests.put(bookingURL, json=booking)
    if r.status_code != 200:
        return jsonify({
            "message": "error occurred when stopping booking."
        }), 500
    else:
        r = r.json()
        customerID = r['customerID']
        doctorID = booking['doctorID']
        # no error so send notification to customer
        hostname = "host.docker.internal"  # change to host.docker.internal before building image
        port = 5672  # port of rabbitmq
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        channel = connection.channel()

        # set up exchange name
        exchangename="notification_topic"
        channel.exchange_declare(exchange=exchangename, exchange_type='topic')

        r = requests.get(notificationURL).json()
        nid = r['notifications'][-1]['nid'] + 1

        # notification to customer
        notificationCustomer= {
            "nid" : nid,
            "sender": doctorID,
            "recevier" : customerID,
            "message" : "Appointment has ended."
        }
        
        notificationDoctor= {
            "nid" : nid+1,
            "sender" : doctorID,
            "receiver": doctorID,
            "message" : "Appointment has ended."
        }
        
        notificationCustomer = json.dumps(notificationCustomer, default=str)
        notificationDoctor = json.dumps(notificationDoctor, default=str)
        channel.basic_publish(exchange=exchangename, routing_key="booking.notification", body=notificationCustomer, properties=pika.BasicProperties(delivery_mode = 2))
        channel.basic_publish(exchange=exchangename, routing_key="booking.notification", body=notificationDoctor, properties=pika.BasicProperties(delivery_mode = 2))
        connection.close()

        return jsonify({
            "message": "Booking ended."
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
