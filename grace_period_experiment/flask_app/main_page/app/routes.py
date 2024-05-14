#!/usr/bin/python3
from app import app
import ssl
import os
from flask import Flask
from flask import render_template
from flask import request
import json
from flask_sqlalchemy import SQLAlchemy
from app.models import Test
from sqlalchemy import exc
from app import db
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import datetime

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        results_received = request.get_json()
        print ("Printing resuts")

        #get useragent, timestamp, test_run, test_type, domain_id, status
        results_received=request.get_json()
        
        for key, value in results_received.items():
            ref = get_reference_date(value[4], value[5])
            test = Test(useragent = value[6], start_time = value[2], end_time = value[3], test_run = value[0], test_type = value[4], 
            domain_id = value[5], status = value[1], direction=value[8], browser_type=value[7], test_name = value[8], reference_date = ref)            
            print ("Status: ", value[1])
            try:
                db.session.add(test)

            except exc.IntegrityError as e:
                db.session().rollback()

        db.session.commit()
        print("Total tests")
        tests = Test.query.all()
        print (tests)

    return render_template("index.html")

def get_reference_date(test_type, domain_id):
    
    path = '/home/hira/research/clock_skew_scripts/grace_period_experiment/grace_periods/apps/time' + str(domain_id) + '_securepki_org/'

    with open(path + 'time' + str(domain_id) + '.securepki.org.crt', 'rb') as f:
        pem_data = f.read()
        
    
    cert = x509.load_pem_x509_certificate(pem_data, default_backend())
    
    if test_type == 'notBefore':
        reference_date = cert.not_valid_before
    elif test_type == 'notAfter':
        reference_date == cert.not_valid_after

    ref_date = reference_date.strftime("%a, %d %b %Y %H:%M:%S GMT")

    return ref_date
