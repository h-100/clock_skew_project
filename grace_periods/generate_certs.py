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
def load_root_CA():

    with open('rootCA.crt', 'rb') as f:
        pem_data = f.read()

    root_cert = x509.load_pem_x509_certificate(pem_data, default_backend())


    with open('rootCA.key', 'rb') as f:
        pem_data = f.read()

    root_private_key = load_pem_private_key(pem_data, password=None, backend=default_backend())

    return root_private_key, root_cert
        
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

def load_root_key():
        
    with open(os.getcwd() + '/rootCA.key', "rb") as key_file:
         private_key = serialization.load_pem_private_key(
             key_file.read(),
             password=None,
             backend=default_backend()
         )
         
    return private_key
        
def generate_cert(notBefore, notAfter, domain_name, root_key):
    
    #generate key for the certificate
    key = generate_key(os.getcwd(), domain_name)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    with open(domain_name + ".key", 'wb') as pem_out:
        pem_out.write(pem)
        
    ##create a root certificate
    subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"MA"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u"Boston"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Northeastern"),
            x509.NameAttribute(NameOID.COMMON_NAME, domain_name),
            ])
    cert = x509.CertificateBuilder().subject_name(
         subject
     ).issuer_name(
         issuer
     ).public_key(
         key.public_key()
     ).serial_number(
         x509.random_serial_number()
     ).not_valid_before(
         notBefore
     ).not_valid_after(
         notAfter
    ).add_extension(
         x509.SubjectAlternativeName([
         x509.DNSName(domain_name),
         x509.DNSName("www." + domain_name),
         ]),
         critical=False,
     
     ).sign(root_key, hashes.SHA256(), default_backend())
    
    # Write our certificate out to disk.
    cert_path = os.getcwd() + "/" + domain_name + ".crt"
    
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
        
    
            
    #subprocess.call('cp -a ' + domain_name + '.pem ' + domain_name + '.crt', shell=True)  
    
def main():
    
    if len(sys.argv) < 3:
        print ("Usage: %s num_certs hours_from_now ", sys.argv[0])
        sys.exit()
            
    num_certs = int(sys.argv[1])
    hours_from_now = int(sys.argv[2])
    
    
    base_time = datetime.datetime.utcnow() + datetime.timedelta(hours=hours_from_now)
    
    
    root_key = load_root_key()
    
    for i in range(num_certs):
        notAfter = base_time + datetime.timedelta(minutes = i+1)
        notBefore = base_time
        domain_name = "time" + str(i+1) + ".securepki.org"
        generate_cert(notBefore, notAfter, domain_name, root_key)
        
        
    ##create apps equivalent to num_certs; call subprocess which calls a bash script
    
    
        
if __name__ == "__main__":
    main()
