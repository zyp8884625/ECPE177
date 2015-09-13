import argparse
import sys
import socket
import os
import string
import sys
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
    parser.add_argument('--bass', metavar = 'BASS_DIR', nargs = 1, default = 'website/html',
                    help = 'Base dir containing website(defualt: website/html')
    parser.add_argument('--port', metavar='PORT', type=int, nargs = 1, default = 8080,
                   help='Port number to listen on(default:8080)')
    args = parser.parse_args()

    path = args.bass
    port = args.port
#--------------------------
    flag = True
    #HTTP Header
    httpheaderOK = b'''HTTP/1.1 200 OK 
    Context-Type: text/html 
    Server: Python version 1.0 
    Connection: Closed\n\n'''
    
    httphearderNotFound = b'HTTP/1.1 404 Not Found '
    # Response function
    def HttpResponse(whtml):
        try:
            server_response = b''
            file_handler = open(whtml,'rb')
            response_content = file_handler.read()
            server_response += httpheaderOK
            server_response +=  response_content
            file_handler.close()
            return server_response
        except Exception as e:
            server_response = httphearderNotFound
            print(e);
            return server_response
            
        
    
    
    

#create Socket object
    try:
        socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Error: could not create socket")
        print("Description: " + str(msg))
        sys.exit()

# Bind to listening port
    try:
        host=''  # Bind to all interfaces
        socketObj.bind((host,port))
    except socket.error as msg:
        print("Error: unable to bind on port %d" % port)
        print("Description: " + str(msg))
        sys.exit()
# Listen
    try:
        backlog=10  # Number of incoming connections that can wait
                    # to be accept()'ed before being turned away
        socketObj.listen(backlog)
    except socket.error as msg:
        print("Error: unable to listen()")
        print("Description: " + str(msg))
        sys.exit()    

    print("Listening socket bound to port %d" % port)
    #try: continue receive data 
    while True:
     # Accept an incoming request
        try:
            (client_s, client_addr) = socketObj.accept()
            # If successful, we now have TWO sockets
            #  (1) The original listening socket, still active
            #  (2) The new socket connected to the client
        except socket.error as msg:
            flag = False
            print("Error: unable to accept()")
            print("Description: " + str(msg))
            sys.exit()
    
        #print("Accepted incoming connection from client")
        #print("Client IP, Port = %s" % str(client_addr))
    
        # Receive data
        try:
            buffer_size = 4096
            raw_bytes = client_s.recv(buffer_size)
        except socket.error as msg:
            flag = False
            print("Error: unable to recv()")
            print("Description: " + str(msg))
            sys.exit()
    
        string_unicode = raw_bytes.decode('ascii')
#         print("Received %d bytes from client" % len(raw_bytes))
#         print("Message contents: \n")
#         print("%s" % string_unicode)
        
        # Decoding HTTP header 
        
        #dirGet = string_unicode.rsplit()
        #print(dirGet)
        dirGet = "/"
        dirGet = string_unicode.rsplit()[1]
        print(dirGet)
        print("Servering file: " + dirGet)
        if dirGet == "/":
            sdata = HttpResponse(path+"/index.html")
        else:
            sdata = HttpResponse(path+dirGet)
            
        # send data
        try:  
            client_s.send(sdata)
        except socket.error as msg:  
            flag = False
            print ("Error sending data")
            print("Description: " + str(msg))
            sys.exit()  
            
        if (flag == False):
            break
    
    # Close both sockets
    
    try:
        client_s.close()
        socketObj.close()
    except socket.error as msg:
        flag = False
        print("Error: unable to close() socket")
        print("Description: " + str(msg))
        sys.exit()
 
    print("Sockets closed, now exiting")

if __name__ == "__main__":
    sys.exit(main())