#!/usr/bin/python3

from app import app, db
import ssl
from app.models import Test
from flask_cors import CORS, cross_origin


###define ssl context
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('time.securepki.org.crt', 'time.securepki.org.key')
CORS(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Test': Test}


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  #response.headers.add('Content-Type', 'application/x-x509-ca-cert')
  return response

if __name__ == "__main__":
    app.run(debug=True, ssl_context=context, host='127.0.0.1', port='443')

