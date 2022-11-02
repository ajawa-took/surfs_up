from flask import Flask

appBob = Flask(__name__)

@appBob.route('/')
def not_funny():
    return "sneasels are extremely serious"













