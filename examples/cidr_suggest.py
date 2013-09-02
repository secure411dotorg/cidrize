#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: ./cidr_suggest.py 1.2.3.4

A script to help people who cant calculate CIDR boundaries in their head.
Use case: User provides a single IPv4 address, script displays all common CIDRs the address is within.
Typically used when studying data about hosts, assists in expanding the data viewed to include 
surrounding netblocks.
Modified from the original script by Jathan McCollum which strictly validates IP addresses.  
"""

__version__ = '0.1'
__author__ = 'Jathan McCollum <jathan+bitbucket@gmail.com> and April Lorenzen https://service.DissectCyber.com'

from cidrize import cidrize, output_str
from netaddr import spanning_cidr
from optparse import OptionParser
import re
import sys

_SELF = sys.argv[0]
DEBUG = False


def validate_cidr(cidr):
    """
    Made for use with jquery.autocomplete. Two matches are returned separated by newlines 
    in the format "network|status": 

        1. The precise calculated networks based on the input range, (Strict)
        2. The maximum spanning CIDR between the first and last IPs. (Loose)

    Example:
        input: 
            16.17.18.19-29

        output:
            16.17.18.19/32, 16.17.18.20/30, 16.17.18.24/30, 16.17.18.28/31|ok
            16.17.18.16/28|ok
    """
    mycidr = output_str(cidr)
    if not re.match(r'^\d+', mycidr):
        return "|%s" % mycidr
    return mycidr + "|ok"

def output_both(cidr, validate=False):
    if validate:
        func = validate_cidr
    else:
        func = output_str

    ret = func(cidr)
    if len(cidr) > 1:
        ret += '\n' + func([spanning_cidr(cidr)])

    return ret

def main():
  for x in ['32', '31', '30', '29', '28', '27', '26', '25', '24', '23', '22', '21', '20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10', '9', '8']:
    ipaddr = []
    try:
        ipaddr = sys.argv[1] + '/' + x
    except IndexError:
        print "usage: %s 1.2.3.4" % _SELF
        sys.exit(-1)

    try:
        cidr = cidrize(ipaddr, modular=False)
        if cidr:
            print output_both(cidr, validate=True)
    except IndexError, err:
        sys.exit(-1)
    
if __name__ == '__main__':
    main()
