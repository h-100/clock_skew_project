from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import datetime
import uuid
import ipaddress
from cryptography.x509.oid import ExtensionOID
import subprocess
from subprocess import Popen, PIPE
import argparse
import pdb
import sys
import os
import shlex
import time
from subprocess import Popen, PIPE, STDOUT
import _thread
import pdb
import threading
def generate_root_CA():
    """
    a) generate rootCA key
    b) generate rootCA crt
    """

    ##generating root key

    root_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend())


    ##self-sign and generate the root certificate

    root_public_key = root_private_key.public_key()
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'Northeastern SSL Test CA'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'Northeastern'),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, u'SSL Clock Skews'),
    ]))

    builder = builder.issuer_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'Northeastern SSL Test CA'),
    ]))
    builder = builder.not_valid_before(datetime.datetime.today() - datetime.timedelta(days=1))
    builder = builder.not_valid_after(datetime.datetime(2019, 12, 31))
    builder = builder.serial_number(int(uuid.uuid4()))
    builder = builder.public_key(root_public_key)
    builder = builder.add_extension(
    x509.BasicConstraints(ca=True, path_length=None), critical=True,)

    root_certificate = builder.sign(
        private_key=root_private_key, algorithm=hashes.SHA256(),
        backend=default_backend()
    )


    ##write to disk
    


    with open("rootCA.key", "wb") as f:
        f.write(root_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("rootCA.crt", "wb") as f:
        f.write(root_certificate.public_bytes(
            encoding=serialization.Encoding.PEM,
        ))

    return root_private_key, root_certificate

def load_root_CA():

    with open('rootCA.crt', 'rb') as f:
        pem_data = f.read()

    root_cert = x509.load_pem_x509_certificate(pem_data, default_backend())


    with open('rootCA.key', 'rb') as f:
        pem_data = f.read()

    root_private_key = load_pem_private_key(pem_data, password=None, backend=default_backend())

    return root_private_key, root_cert


def generate_key(domain_name):
    """
    a) generate key for the certificate being created
    """
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

     #storing client's private key
    with open(domain_name + ".key", "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
     ))

    return key

def generate_csr(key, domain_name):
    """
    generate csr for the client certificate
    """
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    # Provide various details about who we are.
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"MA"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Boston"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Northeastern"),
        x509.NameAttribute(NameOID.COMMON_NAME, domain_name),
    ])).add_extension(
        x509.SubjectAlternativeName([
        x509.DNSName(domain_name),
    ])
    ,
    critical=True,

    # Sign the CSR with our private key.
    ).sign(key, hashes.SHA256(), default_backend())


    # Write our CSR out to disk.
    with open(domain_name + ".csr", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    return csr

def collect_results():
    pass

    """build table as python or latex"""
    x = PrettyTable()    
    x.field_names = [device_name] + thresholds
    
   # "Chrome," + test_type + "," + str(notAfter_date) + "," + thresholds[index], ",fail"
    
    ##read all Chromep entries
    ##get all test_type rows
    ##loop rows
    ##show table

def add_tests_to_main_page(domains, test_type, direction):
    
    list_string = ''
    
    for domain in domains:
        num = domain.split(".")[0].replace('time', '')
        list_string += '"' + str(num) + '",'
        
    list_string.strip(",")
    list_string = "var list = [" + list_string + "]; \n var test_type = '" + test_type + "'; \n var direction = '" + direction + "'; \n"     
    
    with open('/home/hira/research/flask_app/main_page/app/templates/preinclude.txt', 'r') as f:
        pre = f.read()
    
    with open('/home/hira/research/flask_app/main_page/app/templates/postinclude.txt', 'r') as f:
        post = f.read()
        
    complete_html = pre + list_string + post
   
    with open('/home/hira/research/flask_app/main_page/app/templates/include.html', 'w') as f:
        f.write(complete_html)
    
    

def run_browser_automation_web(domains, test_type, browser_type):
    """
    runs the main portal and collects results
    """
    ##running the main page inside the browser to collect results
    if browser_type == "Chrome":
        cmd = 'google-chrome --no-sandbox https://time.securepki.org'
        subprocess.call(cmd, shell=True)
        
    if browser_type == "Firefox":
        cmd = 'firefox https://time.securepki.org'
        subprocess.call(cmd, shell=True)
  
        
def run_chrome_automation(domains, thresholds, notAfter_date, test_type):
    """
    runs domain and returns results

    """
    
    f = open('out.txt', 'w') 

    for index, domain in enumerate(domains):        
        cmd = "nodejs /home/hira/check_pup.js https://" + domain
        args = shlex.split(cmd)
        proc = Popen(args, stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        exitcode = proc.returncode
        
        if b"ERR_CERT_DATE_INVALID" in out:
            f.write("Chrome," + test_type + "," + str(notAfter_date) + "," + str(thresholds[index]) + ",fail")
            f.write("\n")
            
        elif len(out) == 0:
            f.write("Chrome," + test_type + "," + str(notAfter_date) + "," + str(thresholds[index]) + ",pass")
            f.write("\n")
        
def sign_certificate_request(csr, rootkey, rootcrt, client_key, domain_name, notBefore, notAfter):
    """
    generate the certificate based on the csr created
    """

    serial_number = int(str(uuid.uuid4().int)[:20])
    crt = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        rootcrt.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        serial_number  # pylint: disable=no-member
    ).not_valid_before(
        notBefore
    ).not_valid_after(
        notAfter
    ).add_extension(
        extension=x509.KeyUsage(
            digital_signature=True, key_encipherment=True, content_commitment=True,
            data_encipherment=False, key_agreement=False, encipher_only=False, decipher_only=False, key_cert_sign=False, crl_sign=False
        ),
        critical=True
    ).add_extension(
        extension=x509.BasicConstraints(ca=False, path_length=None),
        critical=True
    ).add_extension(
        extension=x509.AuthorityKeyIdentifier.from_issuer_public_key(rootkey.public_key()),
        critical=False
    ).add_extension(
       csr.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_ALTERNATIVE_NAME).value,
       critical=False,
    ).sign(
        private_key=rootkey,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    ##storing client's .crt
    with open(domain_name + ".crt", 'wb') as f:
        f.write(crt.public_bytes(encoding=serialization.Encoding.PEM))

def run_app(num):
        
    cmd = "echo gandalf287 | sudo python3 /home/hira/research/clock_skew_scripts/grace_periods/apps/time" + str(num) + "_securepki_org/app.py"
    subprocess.call(cmd, shell=True)
    
def deploy_apps(domain_names):
    
    # ~ p1 = subprocess.Popen(["./launch_create_apps.sh", str(len(domain_names))],  stdout=open('/dev/null', 'w'),
                 # ~ stderr=open('logfile.log', 'a'),
                 # ~ preexec_fn=os.setpgrp, shell=True)

    # ~ cmd = 'echo gandalf287 | ./create_apps.sh ' + str(len(domain_names)) + ' &'
  
    # ~ cmd = './launch_create_apps.sh'
    # ~ #x = subprocess.check_output(cmd, shell=True)
    # ~ #cmd = ['./launch_create_apps.sh', str(len(domain_names))]
    
    # ~ p = subprocess.Popen([cmd])
    
            # while p1.poll() is None:
                # print('Still sleeping')
                # time.sleep(1)
    
    cmd = 'nohup ./create_apps.sh ' + str(len(domain_names)) + ' &'        
    subprocess.call(cmd, shell=True)
    print ("Done")
    # ~ for i in range(len(domain_names)):
        # ~ t = threading.Thread(target=run_app, args=(i,))
        # ~ threads.append(t)
        # ~ t.start()
   
    
def output_result_in_log(result):
    pass
    

def run_firefox_automation(domain_names, test_type):
    pass

def wait_until_time(wait_till):
    print ("Inside funciton")
    current_time = datetime.datetime.utcnow()
    delta = wait_till - current_time
    print (delta.seconds)
    time.sleep(delta.seconds)
    print ("Sleeping done")
    return

def main():

    parser = argparse.ArgumentParser(description='Launch the grace period experiment')
    parser.add_argument('--device', help='the device to check', type=str, nargs='?', default=0)
    parser.add_argument('--domain_num', help='number of domains', type=str, nargs='?', default=0)
    parser.add_argument('--domain_name', help='domain_name', type=str, nargs='?', default=0)
    parser.add_argument('--timetorun', help='number of minutes from now', type=str, nargs='?', default=0)
    parser.add_argument('--test_type', help='type of test i.e whether its a test to check a notBefore grace period or a notAfter grace period', type=str, nargs='?', default=0)
    parser.add_argument('--test_direction', help='left or right of the current num', type=str, nargs='?', default=0)

    args = parser.parse_args()
    domain_names = []
    thresholds = []

    if not os.path.isfile('rootCA.crt'):
        root_key, root_crt = generate_root_CA()

    else:
        root_key, root_crt = load_root_CA()

    if args.test_type == "notBefore":
        
        notAfter = datetime.datetime.utcnow() + datetime.timedelta(days = 30)
        
        for i in range(int(args.domain_num)):
            split_name = args.domain_name.split(".")
            domain_name = split_name[0] + str(i) + "." + ".".join(split_name[1:])
            domain_key = generate_key(domain_name)
            domain_csr = generate_csr(domain_key, domain_name)
            
            ##setting up the notBefore daten 
            if args.test_direction == 'left':
                notBefore = datetime.datetime.utcnow() + datetime.timedelta(minutes = int(args.timetorun) - i)
            if args.test_direction == 'right':
                notBefore = datetime.datetime.utcnow() + datetime.timedelta(minutes = int(args.timetorun) + i)
            
            sign_certificate_request(domain_csr, root_key, root_crt, domain_key, domain_name, notBefore, notAfter)
            domain_names.append(domain_name)
            thresholds.append(str(i))
    
        base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes = int(args.timetorun))
        add_tests_to_main_page(domain_names, args.test_type, args.test_direction)
        pdb.set_trace()
        #deploy_apps(domain_names)
            
        if args.device == "Chrome":
            wait_until_time(base_time)
            run_browser_automation_web(domain_names, "notBefore", "Chrome")

        if args.device == "Firefox":
            wait_until_time(base_time)
            run_browser_automation_web(domain_names, "notBefore", "Firefox")

    if args.test_type == "notAfter":
        notBefore = datetime.datetime.utcnow() - datetime.timedelta(days = 4)
        
        ##to the right and center of the notAfter date            
        for i in range(int(args.domain_num)):
            split_name = args.domain_name.split(".")
            domain_name = split_name[0] + str(i) + "." + ".".join(split_name[1:])
            domain_key = generate_key(domain_name)
            domain_csr = generate_csr(domain_key, domain_name)
            
            ##setting up the notAfter date
            if args.test_direction == 'left':
                notAfter = datetime.datetime.utcnow() + datetime.timedelta(minutes = int(args.timetorun) - i)
            elif args.test_direction == 'right':
                notAfter = datetime.datetime.utcnow() + datetime.timedelta(minutes = int(args.timetorun) + i)
                
            sign_certificate_request(domain_csr, root_key, root_crt, domain_key, domain_name, notBefore, notAfter)
            domain_names.append(domain_name)
            thresholds.append(str(i))
            
        ##to the left of the notAfter date
        base_time = datetime.datetime.utcnow() + datetime.timedelta(minutes = int(args.timetorun))
        add_tests_to_main_page(domain_names, args.test_type, args.test_direction)
        pdb.set_trace()
        #run main page + run ./create_apps manually using domain number
        #deploy_apps(domain_names)    
        
        if args.device == "Chrome":
            wait_until_time(base_time)
            run_browser_automation_web(domain_names, "notAfter", "Chrome")
            
        if args.device == "Firefox":
            wait_until_time(base_time)
            run_browser_automation_web(domain_names, "notAfter", "Firefox")


if __name__ == "__main__":
    main()
