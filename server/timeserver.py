#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date Thu Jun 11 18:27:20 2020
@author Abdoul Karim TOURE
@contact contact@trabdlkarim.com
@copyright Copyright 2020, Abdoul Karim TOURE
@license GPL v3.0 or Later
@version 1.0.1
@status Development
"""

import os
import sys
import threading
import time
import datetime
import argparse as arg
from socketserver import TCPServer
from socketserver import StreamRequestHandler

HOST = "127.0.0.1"
PORT = 10020

TIMEZONE = "UTC+3"   # Zaman dilimi degiskeni

GREEN = '\033[92m'
END = '\033[0m'

class TimeServerRequestHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.wfile.write(self.data.upper())



class NTPServer:
    def __init__(self,server_address, HandlerClass):
        self.server = TCPServer(server_address, HandlerClass)

    def start_server(self):
        self.server_pid = os.getpid()
        with open("pid.txt","w") as pfile:
            pfile.write(str(self.server_pid)+"\n")
        with self.server:
            self.server.serve_forever()

    @staticmethod
    def stop_server():
        with open("pid.txt",'r') as pfile:
            pid = pfile.readline()
            pid = int(str(pid).strip())

    @staticmethod
    def parse_args(argv):
        parser = arg.ArgumentParser(prog="timeserver",description="description: simple NTP server using TCP protocol")
        group = parser.add_mutually_exclusive_group()
        global PORT
        global TIMEZONE
        parser.add_argument("-p","--port",type=int, default=PORT,
                            help="define the server's listening port")
        parser.add_argument("-t","--timezone",type=int, default=TIMEZONE,
                            help="define the server's timezone")
        group.add_argument("--start", action='store_true', help="start the ntp server")
        group.add_argument("--stop",action="store_true", help="stop the ntp server  ")

        parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.1')
        args =  parser.parse_args(argv)
        args = vars(args)
        PORT = args['port']
        TIMEZONE = args['timezone']
        return parser, args


def main(argv):

    parser, args = NTPServer.parse_args(argv)
    if args["start"] == True:
        try:
           server = NTPServer((HOST,PORT), TimeServerRequestHandler)
           server.start_server()
        except (KeyboardInterrupt,SystemExit):
            print("\nServer stopped.")

    elif args["stop"] == True:
        NTPServer.stop_server()

    else:
        parser.print_help()

if __name__=="__main__":
    main(sys.argv[1:])