from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import json
import facebook
# pip install facebook-sdk
from os import environ

# token will expire so if want to run need to generate a new token (expires in 1 hour)
token = 'EAAFQGYXipNABADx4xcEvmoilw2X9gIRxBY9q9J7ILkcxAWLbLgVqbiRCS8MsSyYTr8ZBwXAI3tp2kAfr51dUpcZB6AxHnoToeib8a2T1PbYKMWKeCS5GNeUT2vN0KY2xYQAMs3NHzFCOTRnX5VqkSy7fC1E5pqii2mx3DmJEqZCzl8UUmugtyZBtAozGwS4ZD'
fb = facebook.GraphAPI(access_token=token)

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/promotion', methods=['POST'])
@cross_origin(supports_credentials=True)
def handle_data():
    data = request.get_data()
    promotion = json.loads(data)
    
    
    message = promotion['message']

    # Write a post with message 
    fb.put_object(parent_object='me', connection_name='feed', message=message)

    # Write a post with image + message 
    # fb.put_photo(image=open(photo, 'rb'),
    #                 message=message)

    return(promotion, 201)





if __name__ == '__main__':
    # if want to build the image use 0.0.0.0
    # localhost is for testing locally
    # app.run(host='localhost', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)


