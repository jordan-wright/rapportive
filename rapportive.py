#!/usr/bin/env python

# rapportive.py
# Author: Jordan <jmwright798@gmail.com>

import requests
import json
import logging
import argparse
import sys
import random
import string

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
logger = logging.getLogger('rapportive')
logger.setLevel(logging.INFO)

def ___rand_letters(size):
    return ''.join(random.choice(string.ascii_lowercase) for x in range(size))

def request(email):
    '''

    rapportive_request(email): Sends a query to the undocumented Rapportive API using a random gmail address
                               Returns the response as a dict
    '''
    email_addr = ___rand_letters(5) + '@gmail.com'
    logger.info('Using ' + email_addr)
    profile = {}
    response = requests.get('https://rapportive.com/login_status?user_email=' + email_addr).json()
    if response['status'] == 200 and 'session_token' in response:
        logger.debug('Session token: ' + response['session_token'])
        profile = requests.get('https://profiles.rapportive.com/contacts/email/' + email, 
            headers = {'X-Session-Token' : response['session_token']}).json()
    return profile

def parse_summary(profile):
    '''

    rapportive_summary(profile): Returns a summary of the Rapportive results for an email address
    '''
    summary = ''
    if 'contact' in profile and profile['contact']:
        person = profile['contact']
        if 'name' in person and person['name']:
            summary += 'Name: ' + person['name'] + '\n'
        if 'occupations' in person and person['occupations']:
            for occupation in person['occupations']:
                if 'job_title' in occupation:
                    summary += 'Position: ' + occupation['job_title'] + '\n'
                if 'company' in occupation:
                    summary += 'Company: ' + occupation['company'] + '\n'
        if 'memberships' in person and person['memberships']:
            for membership in person['memberships']:
                if 'site_name' in membership and membership['site_name']:
                    summary += '\t' + membership['site_name'] + ' - '
                if 'profile_url' in membership and membership['profile_url']:
                    summary += membership['profile_url'] + '\n'
    return summary

def ___process_email(email, output_file=None):
    if not output_file: output_file = None
    profile = request(email)
    if 'success' in profile and profile['success'] != 'nothing_useful':
        logger.info('Found match for ' + email)
        summary = parse_summary(profile)
        print summary
        if output_file:
            output_file.write(summary + '\n')

def main():
    '''

    main(): Expect a list of email addresses via stdin and check them with the Rapportive API
            If the --jigsaw flag is set, format the output from the jigsaw.rb tool and check each
            address.
    '''
    parser = argparse.ArgumentParser(description='Check list of emails using Rapportive API')
    parser.add_argument('--output', '-o', type=argparse.FileType('w'), help='Output file to write results to')
    parser.add_argument('--email', '-e', help='Single email address to test')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    if args.verbose: logger.setLevel(logging.DEBUG)
    if args.email:
        ___process_email(args.email, args.output)
    else:
        for line in sys.stdin:
            ___process_email(line, args.output)
        
if __name__ == '__main__':  
    main()