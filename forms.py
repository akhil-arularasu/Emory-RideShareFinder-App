from wtforms import Form, BooleanField, StringField, SelectField, PasswordField, validators, ValidationError, DateField, TimeField
from wtforms.validators import InputRequired, Length, DataRequired, Regexp
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import cgi
from flask_wtf import FlaskForm
import phonenumbers

class rideshareForm(FlaskForm):
    name = StringField('Name:', [validators.Length(min=1, max=26), validators.Regexp('^[A-Za-z\s]+$', message="Name can only be letters")])
    telNumber = StringField('Telephone:', validators=[DataRequired()])
    rideDate = DateField('Ride Date:', validators=[DataRequired()])
    rideTime = TimeField('Ride Time:', validators=[DataRequired()])


    def validate_telNumber(form, telNumber):
        if len(telNumber.data) > 16:
            print("problem2")
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(telNumber.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+telNumber.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')


class queryForm(FlaskForm):
    rideDate = DateField('Ride Date:', validators=[DataRequired()])
    startTime = TimeField('Start Time:', validators=[DataRequired()])
    endTime = TimeField('End Time:', validators=[DataRequired()])

 
class updateForm(FlaskForm):
    name = StringField('Name:', [validators.Length(min=1, max=26), validators.Regexp('^[A-Za-z\s]+$', message="Name can only be letters")])
    telNumber = StringField('Telephone:', validators=[DataRequired()])
    rideDate = DateField('Ride Date:', validators=[DataRequired()])
    rideTime = TimeField('Ride Time:', validators=[DataRequired()])
    foundRide = SelectField('Rideshare Full?', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])

    def validate_telNumber(form, telNumber):
        if len(telNumber.data) > 16:
            print("problem2")
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(telNumber.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+telNumber.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

class suggestionsForm(FlaskForm):
    subject = StringField('Subject:', validators=[DataRequired()])
    comments = StringField('Comments:', validators=[DataRequired()])