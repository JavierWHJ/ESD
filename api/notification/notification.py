from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import pika
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/notifications'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Notification(db.Model):
    __tablename__ = 'notifications'
    nid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(2), nullable=False)
    message = db.Column(db.String(500), nullable=False)

    def __init__(self, nid, userid, message):
        self.nid = nid
        self.userid = userid
        self.message = message

    def json(self):
        return {"nid": self.nid, "userid": self.userid, "message": self.message}


@app.route('/notifications')
def get_noti():
    return jsonify({
        "notifications": [notification.json() for notification in Notification.query.all()]
    })


@app.route('/notifications', methods=['POST'])
def add_notif():
    data = request.get_json()
    notification = Notification(**data)

    try:
        db.session.add(notification)
        db.session.commit()
    except:
        return jsonify({
            "message": "Error occured creating the record"
        }), 500

    return jsonify(notification.json()), 201


@app.route('/notifications/userid=<string:userid>')
def get_notif_by_userid(userid):
    notification = Notification.query.filter_by(userid=userid).first()
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
    app.run(host='0.0.0.0', port=5000, debug=True)
