#!/usr/bin/python3
from app import db
#from sqlalchemy.dialects.postgresql import JSON

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    useragent = db.Column(db.String(120), index=True, unique=False)
    start_time = db.Column(db.String(120), index=True, unique=False)
    end_time = db.Column(db.String(120), index=True, unique=False)
    test_name = db.Column(db.String(120), index=True, unique=False)
    test_run = db.Column(db.String(120), index=True, unique=False)
    test_type = db.Column(db.String(120), index=True, unique=False)
    domain_id = db.Column(db.String(120), index=True, unique=False)
    status = db.Column(db.String(120), index=True, unique=False) #success or failure
    direction = db.Column(db.String(120), index=True, unique=False) #success or failure
    browser_type = db.Column(db.String(120), index=True, unique=False) #type of browser
    reference_date = db.Column(db.String(120), index=True, unique=False) #type of browser

 #   def __init__(self, useragent, timestamp, test_run, test_type, domain_id, status):
 #       self.useragent = useragent
 #       self.timestamp = timestamp
 #       self.test_run = test_run
 #       self.test_type = test_type
 #       self.domain_id = domain_id
 #       self.status = status

    def __repr__(self):
        return '<Test {}>'.format(self.id, self.useragent, self.start_time, self.end_time, self.test_name, self.test_run, self.test_type, self.domain_id, self.status, self.direction, self.browser_type, self.reference_date)
       
