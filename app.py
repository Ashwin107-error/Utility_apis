from flask import Flask,request,json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)               
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathon.db'
db= SQLAlchemy(app)

class UserDetails(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pancard = db.Column(db.String(20), nullable=False)
    mobileNumber=db.Column(db.String(20),nullable=False)
    verified=db.Column(db.Boolean, nullable=True)
    timestamps=db.Column(db.DateTime, nullable=True)
    vendor=db.Column(db.String(100), nullable=False)

    def __init__(self,name,pancard,mobileNumber,vendor):
        self.name=name
        self.pancard=pancard
        self.mobileNumber=mobileNumber
        self.verified=None
        self.timestamps=None
        self.vendor=vendor
    
@app.route('/adduserdetail', methods=['POST'])
def adduserdetail():
    data=json.loads(request.data)
    print(data)
    user=UserDetails(data["name"],data["pancard"],data["mobileNumber"],data["vendor"])
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as ex:       
        return {"Status":"Failure"}
    user=UserDetails.query.filter_by(pancard=data["pancard"]).first()
    return {"Status":"Success", "UserID":user.id} 


@app.route('/getuserdetail/<string:input_number>', methods=['GET'])
def getuserdetail(input_number):
    user=UserDetails.query.filter_by(mobileNumber=input_number).first()
    if user:
        return {"UserID":user.id, "name":user.name, "pancard":user.pancard, "mobileNumber": user.mobileNumber}
    else: 
        return {"Status":"Failure"}

if __name__=="__main__":
    app.run(debug=True)


