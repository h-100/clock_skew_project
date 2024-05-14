from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_der_private_key
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import uuid
import os
import sys
import subprocess
import ipaddress
from builtins import str
from cryptography.x509.oid import ExtensionOID

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
            encryption_algorithm=serialization.BestAvailableEncryption(b"northeastern")
        ))

    with open("rootCA.crt", "wb") as f:
        f.write(root_certificate.public_bytes(
            encoding=serialization.Encoding.PEM,
        ))
        
    return root_private_key, root_certificate
    
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
            encryption_algorithm=serialization.BestAvailableEncryption(b"northeastern"),
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
    
def sign_certificate_request(csr, rootkey, rootcrt, client_key, domain_name):
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
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
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

    import pdb
    pdb.set_trace()

    

def main():
    
    domain_name = "time.securepki.org"
    
    # ~ if not os.path.isfile('rootCA.crt'):
        # ~ root_key, root_crt = generate_root_CA()
    # ~ else:
        # ~ root_key, root_crt = load_root_key()
    
    root_key, root_crt = generate_root_CA()    
    domain_key = generate_key(domain_name)
    csr = generate_csr(domain_key, domain_name)
    sign_certificate_request(csr, root_key, root_crt, domain_key, domain_name)
    

if __name__ == "__main__":
    main()
