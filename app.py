from flask import Flask,request,json,jsonify,make_response
import requests
from flask_cors import CORS,cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

api_v1_cors_config = {
    "origins": "*",
    "methods": ["GET", "POST"],
    #  "allow_headers": ["Authorization","X-Forwarded-For"]
}
app = Flask(__name__)    
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response 
CORS(app, resources={r"/*": api_v1_cors_config})          
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rmlhackathon:2u4|BNdX@13.232.118.161:60198/hackathon'
db= SQLAlchemy(app)

class UserDetails(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pancard = db.Column(db.String(20), nullable=False)
    mobileNumber=db.Column(db.String(20),nullable=False)
    verified=db.Column(db.String(20), nullable=True)
    updated_timestamp=db.Column(db.DateTime, nullable=False)
    vendor=db.Column(db.String(100), nullable=False)

    def __init__(self,name,pancard,mobileNumber,vendor):
        self.name=name
        self.pancard=pancard
        self.mobileNumber=mobileNumber
        self.verified=None
        self.updated_timestamp=func.now()
        self.vendor=vendor

    def to_json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
@app.route('/adduserdetail', methods=['POST'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def adduserdetail():
    data=json.loads(request.data)
    user=UserDetails(data["name"],data["pancard"],data["mobileNumber"],data["vendor"])
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as ex:       
        return {"Status":"Failure"}
    return {"Status":"Success", "UserID":user.id} 


@app.route('/getuserdetail/<string:input_number>', methods=['GET'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def getuserdetail(input_number):
    user=UserDetails.query.filter_by(mobileNumber=input_number,verified=None).all()
    try:
        result = [row.to_json() for row in user]
        return make_response(jsonify({"result": result}), 200)
    except: 
        return {"Status":"Failure"}
    
@app.route("/send_message", methods=["POST"])
@cross_origin(origin='*')
def sendmessage():
    try:
        data = request.json
        print(data,"LATEST HTTTTTTTT")
        name = data["name"]
        phone_no = data["mobile"]
        payload = {
            "phone": phone_no,
            "media": {
                "type": "media_template",
                "template_name": "test_gaurav_7",
                "lang_code": "en",
                "body": [{"text": name}],
            },
        }
        url = 'https://apis.rmlconnect.net/wba/v1/messages'
        params = payload
        response = requests.post(url,data=json.dumps(payload),headers = {
                "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZGVtbyIsInVzZXJuYW1lIjoiUm1sZGVtb3Rlc3QiLCJleHAiOjE5OTY3NTQ0NjYuMTY1LCJlbWFpbCI6ImFrYXNyYW5qYW5AZ21haWwuY29tIiwib3JpZ19pYXQiOjE1NzEwNDg0NjQsImN1c3RvbWVyX2lkIjoiOWlyNURnN2J2c0NBIiwiaWF0IjoxNjg1NzE0NDY2fQ.3xHE1hVmZ734M6drYG3PWqoXM1qdU1ne7sB5XmGyGGk",
                "Content-Type": "application/json"
            })
        return {"Status": "Success"}

    except Exception as ex:
        print(ex)
        return {"status": "Failure"}
    

@app.route('/getUser/<int:input_user_id>', methods=['GET'])
@cross_origin(origin='*',headers=['Content- Type','Authorization'])
def getUser(input_user_id):
    userInfo=UserDetails.query.filter_by(id=input_user_id).all()
    try:
        result = [row.to_json() for row in userInfo]
        return make_response(jsonify({"result": result}), 200)
    except Exception as ex:
        return {"Status":"Failure"}

if __name__=="__main__":
    app.run(debug=True)


