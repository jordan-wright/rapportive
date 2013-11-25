#!/usr/bin/env python
"""
usage: rapportive.py [-h]
                     [--output OUTPUT]
                     [--email EMAIL]
                     [--verbose]

Check list of emails using Rapportive API

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file to write results to
  -e EMAIL, --email EMAIL
                        Single email address to test
  -v, --verbose
"""

# rapportive.py
# Author: Jordan <jmwright798@gmail.com>

import sys
import logging
from textwrap import dedent

# Requests, from python-requests.org
import requests
from docopt import docopt


# pylint: disable=C0103
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# pylint: enable=C0103

STATUS_URL = 'https://rapportive.com/login_status?user_email={0}'
URL = 'https://profiles.rapportive.com/contacts/email/{0}'


# pylint: disable=R0903
class Profile(object):
    """
    Profile object for collecting profile information before printing
    """
    def __init__(self, person):
        if person:
            self.name = person.get('name')
            self.jobinfo = [
                (occupation.get('job_title'), occupation.get('company'))
                for occupation in person.get('occupations', [])
            ]

            self.memberships = [
                (membership.get('site_name'), membership.get('profile_url'))
                for membership in person.get('memberships', [])
            ]

    def __str__(self):
        return dedent("""
            Name: {0}
            {1}
            {2}
        """).format(
            self.name,
            "\n".join(
                "{0} {1}".format(title, company)
                for title, company in self.jobinfo),
            "\n".join(
                "\t{0} {1}".format(site_name, url)
                for site_name, url in self.memberships)
        )


def request(email):
    '''
    rapportive_request(email): Sends a query to the undocumented Rapportive API
                               Returns the response as a dict
    '''
    status_url = STATUS_URL.format(email)
    response = requests.get(status_url).json()
    session_token = response.get('session_token')
    if response['status'] == 200 and session_token:
        logger.debug('Session token: {0}'.format(session_token))
        url = URL.format(email)
        headers = {'X-Session-Token': session_token}
        return Profile(requests.get(url, headers=headers).json().get('contact'))
    return {}


def parse_summary(profile):
    '''
    rapportive_summary(profile): Returns a Profile object for an email address
    '''
    return Profile(profile.get('contact'))


def ___process_email(email, output_file=None):
    """
    Find email address in rapportive and print profile info
    if found
    """
    profile = request(email)
    success = profile.get('success')
    if success != 'nothing_useful':
        logger.info('Found match for {0}'.format(email))
        summary = parse_summary(profile)
        print(summary)
        if output_file:
            output_file.write(summary + '\n')
    else:
        print("No information found\n")


def main():
    '''
    main(): Expect a list of email addresses via stdin
            and check them with the Rapportive API
    '''
    options = docopt(__doc__, version="0.1.0")

    logging.basicConfig(
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M')
    
    if options["--verbose"]:
        logger.setLevel(logging.DEBUG)

    email = options.get("--email")
    args = [email] if email else [line.rstrip() for line in sys.stdin]
    output = options.get("--output")
    output = output and open(output, "w")
    for arg in args:
        ___process_email(arg, output)


if __name__ == '__main__':
    main()
