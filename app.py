from flask import Flask,request,json,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)               
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
def getuserdetail(input_number):
    user=UserDetails.query.filter_by(mobileNumber=input_number,verified=None).all()
    if user:
        result = [row.to_json() for row in user]
        return make_response(jsonify({"result": result}), 200)
    else: 
        return {"Status":"Failure"}

if __name__=="__main__":
    app.run(debug=True)


