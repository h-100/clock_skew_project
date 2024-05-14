import pdb
from app import db
from app.models import Test
from prettytable import PrettyTable
import sys
import argparse
"""
Chrome_desktop
not After --> 0 --> future --> fail
notAfter --> 0 ---> past

"""
def main():

    """
    #Linux --> browser_type --> Chrome, Firefox
    #Android --> browser_operating system; Chrome_android_mobile
    #iOS --> browser_platform; Safari_mobile
    #Windows --> browser_desktop_test_redo --> browser_desktop_test_redo
    #Mac --> browser_


    """
    parser = argparse.ArgumentParser(description='print the results in a table format')
    parser.add_argument('--test_type', help='the device to check', type=str, nargs='?', default='none')
    parser.add_argument('--browser_type', help='call by the string given to the platform field given in the script launch_grace_periods_exp', type=str, nargs='?', default='none')
    args = parser.parse_args()

    tests = Test.query.all()

    t = PrettyTable(['Test#', 'Browser Type', 'Test Type', 'Direction', 'XMinutesFromStartOfExp', 'Status'])

    i=0
    for test in tests:
        #increment row
        i+=1
        if test.browser_type == args.browser_type and test.test_type == args.test_type:
            if test.direction == 'left':
                t.add_row([i, test.browser_type, test.test_type, 'past', test.domain_id, test.status])
                print("")

            if test.direction == 'right':
                t.add_row([i, test.browser_type, test.test_type, 'future', test.domain_id, test.status])


        # ~ if test.browser_type == 'Firefox' and test.test_type == test_type:
            # ~ if test.direction == 'left':
                # ~ t.add_row([i, test.browser_type, test.test_type, 'past', test.domain_id, test.status])

            # ~ if test.direction == 'right':
                # ~ t.add_row([i, test.browser_type, test.test_type, 'future', test.domain_id, test.status])



    print (t)


if __name__ == "__main__":
    main()
