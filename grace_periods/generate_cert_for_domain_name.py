import generate_certs
import sys
import datetime

def main():
    
    domain_name = sys.argv[1]
    root_key, root_crt = generate_certs.load_root_CA()
    notBefore = datetime.datetime.now()
    notAfter = notBefore + datetime.timedelta(days = 2)
    domain_key = generate_certs.generate_key(domain_name)
    domain_csr = generate_certs.generate_csr(domain_key, domain_name)
    generate_certs.sign_certificate_request(domain_csr, root_key, root_crt, domain_key, domain_name, notBefore, notAfter)
    
if __name__ =="__main__":
    main()


