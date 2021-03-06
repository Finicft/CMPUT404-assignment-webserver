#  coding: utf-8 
import socketserver
import os
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Fangting Chen
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        method = None 
        status_code = None 
        mime_type = None 
        content = None 


        self.data = self.request.recv(1024).strip()
        #string data 
        data = self.data.decode().split("\r\n")
        header = data[0].split(" ")   

        #GET METHOD 
        method = header[0]
        #GET path 
        file_path = os.path.abspath(os.getcwd() + "/www" + header[1])
        if os.path.isdir(file_path) and header[1][-1] != "/":
            file_path += "/index.html"
            status_code = "301 Permanently moved to {}\r\n".format(file_path)

        if header[1][-1] == "/":
            file_path += "/index.html"
 

        #GET PROTOCOL  
        protocol = header[2] 

       #GET MIME TYPE
       #https://stackoverflow.com/questions/14412211/get-the-mimetype-of-a-file-with-python
        mime_type = mimetypes.guess_type(file_path)[0]
        if mime_type == None:
            mime_type = "text/html"
        mime_type = "Content-Type: " + mime_type + "\r\n"
        

        #GET STATUS CODE AND CONTENT 
        if method != "GET":
            status_code = "405 Method Not Allowed\r\n"
            content = "<h1>{}</h1>".format(status_code)
            
        else:
            #https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
            if os.path.isfile(file_path) and "www" in file_path :
                if status_code == None:
                    status_code = "200 OK\r\n"
                   
                content = open(file_path, "r").read()


            else: 
                status_code = "404 Not Found"
                content = "<h1>404 NOT FOUND</h1>"

                #content = "<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<title>{}</title>\r\n</head>\r\n</html>".format(status_code)

    

        #SEND 
        reponse = protocol + " " + status_code + mime_type + "\r\n" + content + "\r\n"
        self.request.sendall(reponse.encode())

        
    
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
