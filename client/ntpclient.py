#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date Fri Jun 12 01:32:14 2020
@author Abdoul Karim TOURE
@contact contact@trabdlkarim.com
@copyright Copyright 2020, Abdoul Karim TOURE
@license GPL v3.0 or Later
@version 1.0.1
@status Development
"""

import socket
import time
import argparse as arg
import sys
import os

HOST = "127.0.0.1"
PORT = 10020
data = "Hello Time Server"


class NTPClient(object):
    def __init__(self,server_address):
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def get_time(self):
        with self.socket:
            self.socket.connect(self.server_address)
            self.socket.sendall(bytes(data+"\n","utf-8"))
            received =  str(self.socket.recv(1024),"utf-8")
        print("Sent: {}".format(data))
        print("Received: {}".format(received))

    def set_sys_time(self):
        pass

    @staticmethod
    def parse_args(argv):
        parser = arg.ArgumentParser(prog="ntpclient",description="description: simple NTP client using TCP")
        parser.add_argument("-p","--port",type=int, default=PORT,help="server listening port")
        parser.add_argument("-r","--remote", default=HOST, help="remote host IP address ")
        parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.1')
        args =  parser.parse_args(argv)
        args = vars(args)
        return args


def main(argv):
    args = NTPClient.parse_args(argv)
    ntp = NTPClient((args['remote'],args['port']))
    ntp.get_time()

if __name__=="__main__":
    main(sys.argv[1:])