from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pika
import requests
app = Flask(__name__)
CORS(app)

prescriptionURL = "http://prescription:5000/prescription"


@app.route('/make_prescription', methods=['POST'])
def make_prescription():
    #example data
    # {
    #   bookingID : 1
    #   doctorID : d1
    #   customerID :c3
    #   prescription : 1 panadol per day
    #   nid : 3
    # )
    data = request.get_json()
    prescription = json.loads(json.dumps(data, default=str))
    r = requests.post(prescriptionURL, json=prescription)
    if r.status_code != 200:
        return jsonify({
            "message": "error sending to prescription"
        }), 500
    else:
        customerID = data['customerID']
        hostname = "host.docker.internal"
        port = 5672
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        channel = connection.channel()

        exchangename = "notification_topic"
        channel.exchange_declare(exchange=exchangename, exchange_type="topic")
        notification = {
            "nid" : data['nid'],
            "userid": customerID,
            "message" : "You have a new prescription"
        }

        notification = json.dumps(notification, default=str)
        channel.basic_publish(exchange=exchangename, routing_key="prescription.notification", body=notification, properties=pika.BasicProperties(delivery_mode=2))
        connection.close()
        return jsonify({
            "message": "prescription added"
        }),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)