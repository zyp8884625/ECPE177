#!/usr/bin/env python3

import argparse
import sys
from socketThreadstest import socketThreadstest
import os
import string
import sys
import time
import socket
import threading
import time


if not sys.version_info[:2] == (3,4):
    print("Error: need Python 3.4 to run program")
    sys.exit(1)
else:
    print("Using Python 3.4 to run program")

def main():
#set help and default args
    parser = argparse.ArgumentParser(description='HTTP Server for ECPE 177')
    parser.add_argument('--version', action='version', version='1.0',
                   help="show program'socketObj version number and quit")
    parser.add_argument('--base', metavar = 'BASS_DIR', default = 'website/html',
                    help = 'Base dir containing website(defualt: website/html')
    parser.add_argument('--port', metavar='PORT', type=int, default = 8080,
                   help='Port number to listen on(default:8080)')
    parser.add_argument('--verbose', metavar='VERBOSE', type=bool, default = False,
                   help='enable verbose mood')
    args = parser.parse_args()

    path = args.base
    port = args.port
    verbose = args.verbose
    print(port)
#--------------------------

    try:
        socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Error: could not create socket")
        print("Description: " + str(msg))
        sys.exit()
    try:
        host=''  # Bind to all interfaces
        socketObj.bind((host, port))
    except socket.error as msg:
        print("Error: unable to bind on port %d" % port)
        print("Description: " + str(msg))
        sys.exit()
    try:
        backlog=10  # Number of incoming connections that can wait
                    # to be accept()'ed before being turned away
        socketObj.listen(backlog)
    except socket.error as msg:
        print("Error: unable to listen()")
        print("Description: " + str(msg))
        sys.exit()  
    threads = []
    j=0
    while True:
        try:
            (client_s, client_addr) = socketObj.accept()
            threads.append(socketThreadstest('t',port,verbose,path,socketObj,client_s,client_addr))
            for i in range (len(threads)-j):
                threads[i+j].start()
            j += 1
            # If successful, we now have TWO sockets
            #  (1) The original listening socket, still active
            #  (2) The new socket connected to the client
        except socket.error as msg:
            flag = False
            print("Error: unable to accept()")
            print("Description: " + str(msg))
            sys.exit()
    for i in threads:
        i.join()
    
        
    
        
    

    # Use the join() function to wait for a specific thread to finish
    # (i.e. thread1.join() or thread2.join())
    if verbose:
        print("Waiting for all threads to finish")
        print("All threads have finished")

if __name__ == "__main__":
    sys.exit(main())
