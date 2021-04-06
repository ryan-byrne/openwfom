from flask import Flask
import pymongo, os, ssl
from mongoengine import connect, Document, StringField, disconnect

from .api import api

app = Flask('pywfom')
app.secret_key = os.urandom(12).hex()
app.register_blueprint(api, url_prefix='/api')

# TODO: Get credentials from HTTP
pwd = os.environ['MONGODB_PASSWORD']

print('Connecting to MongoDB...')
# TODO: Add individual credentials
connect(host="mongodb+srv://ryan:{}@baseball.am3n7.mongodb.net/pywfom?ssl=true&ssl_cert_reqs=CERT_NONE".format(pwd))

def run_server():
    app.run(debug=True)
    print('Disconnecting from MongoDB')
    disconnect()

def test_server():
    print('test server')
