# import notification
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import requests
import pika
from os import environ
app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/notifications'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
CORS(app)

# class Notification(db.Model):
#     __tablename__ = 'notifications'
#     nid = db.Column(db.Integer, primary_key=True)
#     userid = db.Column(db.String(2), nullable=False)
#     message = db.Column(db.String(500), nullable=False)

#     def __init__(self, nid, userid, message):
#         self.nid = nid
#         self.userid = userid
#         self.message = message

#     def json(self):
#         return {"nid": self.nid, "userid": self.userid, "message": self.message}


hostname = "host.docker.internal" # localhost for testing, host.docker.internal for container
port = 5672
notificationURL = "http://notification:5000/notifications"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
channel = connection.channel()

exchangename="booking_direct"
channel.exchange_declare(exchange=exchangename, exchange_type='direct')

def receiveNotification():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="notification", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='booking.notification') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body):
    data = json.loads(body)
    r = requests.post(notificationURL, json=data)

if __name__ == '__main__':
    receiveNotification()
