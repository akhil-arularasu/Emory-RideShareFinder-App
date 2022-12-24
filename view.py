from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import cgi
from flask_sqlalchemy import SQLAlchemy
from forms import rideshareForm, queryForm
import babel
import dateutil
from dateutil import parser


app = Flask(__name__)

app.secret_key = "hello"
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rides.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permament_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)
class rides(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("Name", db.String(100))
    telNumber = db.Column("TelephoneNumber", db.Integer)
    rideDate = db.Column("Date", db.Integer)
    rideTime = db.Column("Departure Time", db.Time)


def __init__(self, name, telNumber):
    self.name = name
    self.telNumber = telNumber

@app.route("/capture", methods=["POST", "GET"])
def capture():
    if request.method == "POST":
        '''
        individualName = request.form["name"]
        session["name"] = individualName
        telephoneNumber = request.form["telNumber"]
        session["telNumber"] = telephoneNumber
        '''
        thisForm = rideshareForm()
        if thisForm.validate_on_submit():
            currentPerson = rides(name=thisForm.name.data, telNumber=thisForm.telNumber.data, rideDate=thisForm.rideDate.data, rideTime=thisForm.rideTime.data)
            db.session.add(currentPerson)
            db.session.commit()
            return render_template("success.html", form=thisForm)
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
    thisForm = queryForm()
    if request.method == "POST":
        if thisForm.validate_on_submit():
            rides_list = rides.query.filter(rides.rideTime.between(thisForm.startTime.data, thisForm.endTime.data), rides.rideDate == thisForm.rideDate.data)            
            return render_template('queryResult.html', form=thisForm, data=rides_list)
        else:
            return render_template('queryResult.html', form=thisForm)
    else:
        return render_template('queryResult.html', form=thisForm)

@app.route("/home")
def home():
    return render_template("home.html")

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



if __name__ == "__main__":
    with app.app_context():     
        db.create_all()
    app.run(debug=True)