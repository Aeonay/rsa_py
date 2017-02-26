#!/usr/bin/env python

from rsa_py import rsa_functions

def main():
    print 'Launching nuke...'
    rsa = rsa_functions.RSAPy(1024)
    original_msg = 1234567890  # Has to be an integer, TODO: implement safe padding
    cipher = rsa.encrypt(original_msg)
    msg = rsa.decrypt(cipher)
    print "origin msg       = {0}".format(original_msg)
    print "cipher msg       = {0}".format(cipher)
    print "decrypted msg    = {0}".format(msg)

main()
