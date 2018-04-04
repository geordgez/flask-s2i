from flask import Flask

myapp = Flask(__name__)

from sampleapp import views

myapp.secret_key = 'my_special_sauce'
