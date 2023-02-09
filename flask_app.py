from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import datetime, timedelta
import cgi
from flask_sqlalchemy import SQLAlchemy
from forms import rideshareForm, queryForm, updateForm
import babel
import dateutil
from dateutil import parser
from model import rides, rides_atl, db
from socket import gethostname

app = Flask(__name__)
app.secret_key = "hello"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permament_session_lifetime = timedelta(minutes=1)

db.app = app
db.init_app(app)

def __init__(self, name, telNumber):
    self.name = name
    self.telNumber = telNumber

@app.route("/capture", methods=["POST", "GET"])
def capture():
    if "college" not in session:
        return render_template("home.html")
    session["error"] = ''
    if request.method == "POST":
        '''
        individualName = request.form["name"]
        session["name"] = individualName
        telephoneNumber = request.form["telNumber"]
        session["telNumber"] = telephoneNumber
        '''
        thisForm = rideshareForm()
        if thisForm.validate_on_submit():
            given_name = thisForm.name.data
            dbRecord = rides.query.filter_by(name=given_name).first()
            if(dbRecord != None):
                session["error"] = "Your ride information already exists in the system. To change your ride details, please go to "
                return render_template("capture.html", form=thisForm)
            given_time = thisForm.rideTime.data
            time_format_str = '%H:%M:%S'
            given_time = datetime.strptime(str(given_time), time_format_str)
            print(type(given_time))
            print(type(given_time.time()))
            given_start_time=(given_time)-timedelta(minutes=30)
            given_end_time=(given_time)+timedelta(minutes=30)
            currentPerson = rides(name=thisForm.name.data, telNumber=thisForm.telNumber.data, rideDate=thisForm.rideDate.data, rideTime=thisForm.rideTime.data, rideFound='N', college=session["college"], fromTo=session["fromTo"], location="ATL Airport")
            db.session.add(currentPerson)
            db.session.commit()
            session["name"] = thisForm.name.data
            rides_list = rides.query.filter(rides.rideTime.between((given_start_time.time()), (given_end_time.time())), rides.rideDate == thisForm.rideDate.data)
            return render_template("success.html", form=thisForm, data=rides_list)

        else:
            return render_template("capture.html", form=thisForm)
    else:
        thisForm = rideshareForm()
        return render_template("capture.html", form=thisForm)

@app.route("/list")
def rideList():
        rides_list = rides.query.all()
        '''
        try:
            ride_text = '<ul>'
            for person in rides_list:
                ride_text += '<li>' + person.name + ' | ' + str(person.telNumber) + ' | ' + str(person.rideDate) + ' | ' + str(person.rideTime) + '</li>'
            ride_text += '</ul>'
            return ride_text
        except Exception as e:
            # e holds description of the error
            error_text = "<p>The error:<br>" + str(e) + "</p>"
            hed = '<h1>Something is broken.</h1>'
            return hed + error_text
        '''
        return render_template('queryResult.html', data=rides_list)

@app.route("/query", methods=["POST", "GET"])
def ridesQuery():
    if "college" not in session:
        return render_template("home.html")
    thisForm = queryForm()
    if request.method == "POST":
        if thisForm.validate_on_submit():
            # create a JSON with 3 form fields.
            # call search microservice with JSON
            # receive the JSON response from microservice and take the JSON data and create rides_list from the JSON data
            # render template
            rides_list = rides.query.filter(rides.rideTime.between(thisForm.startTime.data, thisForm.endTime.data), rides.rideDate == thisForm.rideDate.data, rides.college == session["college"], rides.fromTo == session["fromTo"]).order_by(rides.rideTime)          
            return render_template('queryResult.html', form=thisForm, data=rides_list)
        else:
            return render_template('queryResult.html', form=thisForm)
    else:
        return render_template('queryResult.html', form=thisForm)

@app.route("/")
@app.route("/atl/*")
@app.route("/home")
def home():
    if "college" in session:
        session.pop("college")
    if "fromTo" in session:
        session.pop("fromTo")
    print(request.args.get("college"))
    print(request.args.get("fromTo"))
    if (request.args.get("college")):
        session["college"] = request.args.get("college")
        if request.args.get("fromTo"):
            session["fromTo"] = request.args.get("fromTo")
        return render_template("home.html")
    else:
        return render_template("home.html")   

@app.route("/update", methods=["POST", "GET"])
def update():
    if "college" not in session:
        return render_template("home.html")
    thisForm = updateForm()
    session["error"] = ''
    if request.method == "POST":
        if request.form.get('search'):
            currentPerson = rides.query.filter(rides.college == session["college"], rides.fromTo == session["fromTo"], rides.name == thisForm.name.data).first()
            if(currentPerson == None):
                session["error"] = "The name entered was not found for this combination: " + session["fromTo"] + " " + session["college"] + " Please enter your information below or click Home."
                thisForm = rideshareForm()
                return render_template("capture.html", form=thisForm)
            thisForm.name.data = currentPerson.name
            thisForm.telNumber.data = currentPerson.telNumber
            datetime_str = currentPerson.rideDate
            rideDate = datetime.strptime(datetime_str, '%Y-%m-%d')
            thisForm.rideDate.data = rideDate
            thisForm.rideTime.data = currentPerson.rideTime
            if currentPerson.rideFound == 'Y':
                thisForm.foundRide.data = "Yes"
            else:
                thisForm.foundRide.data = 'No'
            return render_template('update.html', form=thisForm)
        else:
            if thisForm.validate_on_submit():
                currentPerson = rides.query.filter(rides.college == session["college"], rides.fromTo == session["fromTo"], rides.name == thisForm.name.data).first()
                currentPerson.rideDate = thisForm.rideDate.data
                currentPerson.rideTime = thisForm.rideTime.data
                currentPerson.telNumber = thisForm.telNumber.data
                currentPerson.rideFound = 'Y'
                if thisForm.foundRide.data == "No":
                    currentPerson.rideFound = 'N'
                db.session.commit()
                return render_template('updateSuccess.html')
            else:
                return render_template('update.html', form=thisForm)
    else:
        return render_template('update.html', form=thisForm)

@app.template_filter('strfdate')
def _jinja2_filter_date(date, fmt=None):
    date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%b %d, %Y'
    return native.strftime(format) 

@app.template_filter('strftime')
def _jinja2_filter_time(time, fmt=None):
    native = time.replace(tzinfo=None)
    format='%I:%M %p'
    return native.strftime(format) 

'''
@app.template_filter('size')
def findSize(data):
    return data.count()
'''

@app.route("/suggestions", methods=["POST", "GET"])
def suggestions():
    if request.method == "POST":
        if request.form.get('submit'):
            suggestionSubject = request.form['txtsubject']
            commentText = request.form['txtcomment']
            log_message = "Subject: {} and Comment: {}".format(suggestionSubject, commentText)
            save(log_message)
            return render_template('suggestionSuccessPage.html') 
    else:
        return render_template('suggestions.html')

@app.route("/recognition")
def recognition():
    return render_template('recognition.html')

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

def save(text, filepath='suggestions.txt'):
    with open("suggestions.txt", "a") as f:
        f.write(text)        

if __name__ == "__main__":
    with app.app_context():
#        db.drop_all()
        db.create_all()
    if 'liveconsole' not in gethostname():
        app.run(debug=True)