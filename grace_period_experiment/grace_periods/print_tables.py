import pdb
import sys
from app import db
from app.models import Test
from prettytable import PrettyTable
    
def main():
    
    tests = Test.query.all()    
 
    t = PrettyTable(['Browser Type', 'Test Type', 'Direction', 'Status'])
 
    for test in tests:
        if test.browser_type == 'Chrome' and test.test_type == 'notAfter':
            if test.direction == 'left':
                t.add_row([test.browser_type, test.test_type, 'past', test.status])
                
            if test.direction == 'right':
                t.add_row([test.browser_type, test.test_type, 'future', test.status])
         
        if test.brower_type == 'Chrome' and test.test_type == 'notBefore':
            if test.direction == 'left':
                t.add_row([test.browser_type, test.test_type, 'past', test.status])
            if test.direction == 'right':
                t.add_row([test.browser_type, test.test_type, 'future', test.status])
             
        if test.browser_type == 'Firefox' and test.test_type == 'notAfter':
            if test.direction == 'left':
                t.add_row([test.browser_type, test.test_type, 'past', test.status])
                
            if test.direction == 'right':
                t.add_row([test.browser_type, test.test_type, 'future', test.status])
    
         
        if test.brower_type == 'Firefox' and test.test_type == 'notBefore':
            if test.direction == 'left':
                t.add_row([test.browser_type, test.test_type, 'past', test.status])
            if test.direction == 'right':
                t.add_row([test.browser_type, test.test_type, 'future', test.status])
            
    
    print (t)
       
    
if __name__ == "__main__":
    main()    
