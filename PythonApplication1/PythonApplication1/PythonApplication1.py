#!/usr/bin/env python3

# Simple network socket demo - SERVER
#
# Set script as executable via: chmod +x server.py
# Run via: ./server.py <PORT>

import socket
import sys
import argparse

HearderOk = b'''HTTP/1.1 200 OK\r\n Server: Python socket Server\r\n Content-Type: text/html;charset=utf-8\r\n Connection: Closed\r\n\r\n'''
HearderErro = b'''HTTP/1.1 404 NOT FOUND\r\n Server: Python socket Server\r\n\r\n'''
def answer(path):
        resp = b''
        try:    
            file_handler = open(path,'rb') # rb =read as binary code from the path 
            resp_con = file_handler.read() #read file 
            resp = resp+HearderOk  #set the rea[pnse heder to headerok 
            resp = resp+resp_con   #add the file to the response 
            file_handler.close()   # then close the file 
            return server_response 
        except Exception as e: #if the file dosent work 
            resp = resp + HearderErro  #set the responst to header erro
            print(e);
            return resp
def main():
    

    # Tip: You should use argparse - this method
    # is sloppy and inflexible
    parser = argparse.ArgumentParser(description='Web Server for COMP/ECPE 177')
    #parser.add_argument('-h',help='--help show this help message and exit')
    parser.add_argument('--version', help = 'how programs version number and exit')
    parser.add_argument('--base', metavar = 'BASE_DIR', default = 'website/html', help = 'BASE_DIR Base dir containing website')
    parser.add_argument('--port', metavar = 'PORT', type = int, default = 8080, help ='Port number to listen on')
    args = parser.parse_args()
    port = args.port
    path = args.base
    

    #print(args.accumulate(args.integers))
	    
    

    # Create TCP socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Error: could not create socket")
        print("Description: " + str(msg))
        sys.exit()

    # Bind to listening port
    try:
        host=''  # Bind to all interfaces
        s.bind((host,port))
    except socket.error as msg:
        print("Error: unable to bind on port %d" % port)
        print("Description: " + str(msg))
        sys.exit()

    # Listen
    try:
        backlog=10  # Number of incoming connections that can wait
                    # to be accept()'ed before being turned away
        s.listen(backlog)
    except socket.error as msg:
        print("Error: unable to listen()")
        print("Description: " + str(msg))
        sys.exit()    

    print("Listening socket bound to port %d" % port)
    # Accept an incoming request
    while True:
        try:

            (client_s, client_addr) = s.accept()
            # If successful, we now have TWO sockets
            #  (1) The original listening socket, still active
            #  (2) The new socket connected to the client
        except socket.error as msg:
            print("Error: unable to accept()")
            print("Description: " + str(msg))
            sys.exit()
            print("Accepted incoming connection from client")
            print("Client IP, Port = %s" % str(client_addr))

    # Receive data
        try:
            buffer_size=4096
            raw_bytes = client_s.recv(buffer_size)
        except socket.error as msg:
            print("Error: unable to recv()")
            print("Description: " + str(msg))
            sys.exit()

        string_unicode = raw_bytes.decode('ascii')
        print("Received %d bytes from client" % len(raw_bytes))
        print("Message contents: %s" % string_unicode)
    # Decode the Header from clinet
    
        Dir=string_unicode.rsplit()[1]

        if Dir == "/":
            respon = answer(path+"/index.html")
        else:
            respon = answer(path+Dir)
        
        client_s.sendall(respon)
        client_s.close()


    # Close both sockets
    try:
            client_s.close()
            s.close()
    except socket.error as msg:
           print("Error: unable to close() socket")
           print("Description: " + str(msg))
           sys.exit()
           print("Sockets closed, now exiting")

if __name__ == "__main__":
	sys.exit(main())
