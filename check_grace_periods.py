import pdb
import sys
import argparse
import subprocess
import OpenSSL
import ssl
import socket
import datetime
from selenium import webdriver
import time
from pyvirtualdisplay import Display

def get_not_before(domain):

    cert = ssl.get_server_certificate((domain, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    notAfter = x509.get_notAfter().decode('utf-8')
    #20190313081700Z
    ssl_date_fmt = '%Y%m%d%H%M%S'

    notAfterDate = datetime.datetime.strptime(notAfter.strip('Z'), ssl_date_fmt)
    return notAfterDate




def main():
    #get arguments
    #domains in a list
    #time range to test in seconds


    #domains = args.domains
    #time_range = args.time

    domains = ['time.securepki.org']
    time_range = 10

    browsers = ['Chrome']


    ##get the certificate notBefore date

    for domain in domains:
        #format of notBefore --> 20190313081700Z --> YYYYMMDDHHSS00Z
        not_before = get_not_before(domain)
        for browser in browsers:
            if browser == 'Chrome':
                for seconds_to_check in range(time_range):
                    date_to_check = not_before + datetime.timedelta(seconds=seconds_to_check+1)
                    date_to_check = date_to_check.strftime("%d %b %Y %H:%M:%S") #obtain date (notAfter + seconds + 1)
                    cmd = 'sudo date -s "' + str(date_to_check) + '"'
                    ret = subprocess.call(cmd, shell=True)
                    #display = Display(visible=0, size=(800, 600))
                    #display.start()
                    driver = webdriver.Chrome()
                    driver.get('https://' + domain)
                    time.sleep(5)
                    pdb.set_trace()
                    driver.quit()

            if browser == 'Firefox':
                for seconds_to_check in range(time_range):
                    #date_to_check = not_before + datetime.timedelta(seconds=seconds_to_check+1)
                    #date_to_check = date_to_check.strftime("%d %b %Y %H:%M:%S") #obtain date (notAfter + seconds + 1)
                    #cmd = 'sudo date -s "' + str(date_to_check) + '"'
                    #ret = subprocess.call(cmd, shell=True)
                    profile = webdriver.FirefoxProfile()
                    profile.set_preference("browser.ssl_override_behavior", 0)
                    profile.accept_untrusted_certs = False
                    driver = webdriver.Firefox(profile)
                    driver.get('https://' + domain)
                    time.sleep(5)
                    pdb.set_trace()
                    driver.quit()

            if browser == 'Safari':
                pass

            if browser == 'IE':
                pass

#TODO: write code for a Safari selenium driver




if __name__ == "__main__":
    main()
