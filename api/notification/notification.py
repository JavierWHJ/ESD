from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS
import json
from os import environ
import datetime
app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/notifications'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Notification(db.Model):
    __tablename__ = 'notifications'
    nid = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(2), nullable=False)
    receiver = db.Column(db.String(2), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, nid, sender, receiver, message):
        self.nid = nid
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.timestamp = func.now()

    def json(self):
        return {"nid": self.nid, "sender": self.sender, "receiver": self.receiver, "message": self.message, "timestamp": self.timestamp}


@app.route('/notifications')
def get_noti():
    return jsonify({
        "notifications": [notification.json() for notification in Notification.query.all()]
    })


@app.route('/notifications', methods=['POST'])
def add_notif():
    data = request.get_json()
    # add autoincrement 
    allnoti = [notification.json() for notification in Notification.query.all()]
    if len(allnoti) == 0:
        nid = 1
    else:
        # got noti inside
        lastnoti = allnoti[-1]
        lastnoti_id = lastnoti['nid']
        nid = lastnoti_id +1
    
    
    notification = Notification(nid, **data)
    try:
        db.session.add(notification)
        db.session.commit()
    except:
        return jsonify({
            "message": "Error occured creating the record"
        }), 500

    return jsonify(notification.json()), 201


@app.route('/notifications/userid=<string:userid>')
def get_notif_by_receiver(userid):
    notification = Notification.query.filter_by(receiver=userid).first()
    if notification == None:
        return jsonify({}), 200
    return jsonify(notification.json()), 200



@app.route('/notifications/nid=<int:nid>', methods=['DELETE'])
def delete_noti(nid):
    notification = Notification.query.filter_by(nid=nid).first()
    try:
        db.session.delete(notification)
        db.session.commit()
        return jsonify({
            "message": "Successfully deleted record."
        }), 200
    except:
        return jsonify({
            "message": "An error occurred while trying to delete record."
        }), 500


if __name__ == '__main__':
    # app.run(host='localhost', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
    
