#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import cgi

"""
Written by: Raymon Skjørten Hansen
Email: raymon.s.hansen@uit.no
Course: INF-2300 - Networking
UiT - The Arctic University of Norway
May 9th, 2019
"""
input_list = []
messages = []
dict_form_data = dict()
class requestHandler(BaseHTTPRequestHandler):
    """
    This class is responsible for handling a request. The whole class is
    handed over as a parameter to the server instance so that it is capable
    of processing request. The server will use the handle-method to do this.
    It is instantiated once for each request!
    Since it inherits from the StreamRequestHandler class, it has two very
    usefull attributes you can use:

    rfile - This is the whole content of the request, displayed as a python
    file-like object. This means we can do readline(), readlines() on it!

    wfile - This is a file-like object which represents the response. We can
    write to it with write(). When we do wfile.close(), the response is
    automatically sent.

    The class has three important methods:
    handle() - is called to handle each request.
    setup() - Does nothing by default, but can be used to do any initial
    tasks before handling a request. Is automatically called before handle().
    finish() - Does nothing by default, but is called after handle() to do any
    necessary clean up after a request is handled.
    """
    def do_GET(self):
        if self.is_safe_path(self.path):
            if self.path == "/":
                self.serve_file("index.html", "text/html")
            elif self.path.endswith(".py"):
                self.send_forbidden()
            elif self.path.endswith(".md"):
                self.send_forbidden()
            # if self.path == "/messages": #this is the restful API
            #     self.send_response(200)
            #     self.send_header("Content-Type", "application/json")
            #     self.end_headers()
            #     # Return the list of messages as a JSON response
            #     self.wfile.write(json.dumps(messages).encode("utf-8"))
            else:
                # Serve other files within the allowed directory
                filename = self.path[1:]  # Remove the leading "/"
                self.serve_file(filename, "text/plain")  # Adjust content type if needed
        else:
            self.send_forbidden()
        """
        This method is responsible for handling an http-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """
    def do_POST(self):
        # Check if the file 'test.txt' exists
        if not os.path.isfile('test.txt'):
            # Create the file and write data to it
            with open('test.txt', 'w') as file:
                pass
        if self.is_safe_path(self.path):
            print(self.path)
            if self.path == "/test.txt":
                try:
                    content_length = int(self.headers.get('Content-Length'))
                    post_data = self.rfile.read(content_length)
                    print(post_data)
                    
                    # If the file exists, append data to it
                    with open('test.txt', 'a') as file:
                        file.write(post_data.decode('utf-8')[5:])
                        
                    # Read the complete contents of the file
                    with open('test.txt', 'r') as file:
                        file_contents = file.read()
                        
                    # Return the updated file contents in the response with status 200 (OK)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain")
                    self.send_header("Content-Length", str(len(file_contents)))
                    self.end_headers()
                    self.wfile.write(file_contents.encode('utf-8'))
                except Exception as e:
                    self.send_error(500, f"Internal Server Error: {str(e)}")
            else:
                self.send_forbidden()
        else:
            self.send_forbidden()
    def serve_file(self, filename, content_type):
        try:
            with open(filename, "rb") as f:
                content = f.read()
            content_length = len(content)

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(content_length))
            self.end_headers()

            self.wfile.write(content)
        except FileNotFoundError:
            self.send_not_found()
    def is_safe_path(self, path):
        # Check if the path is within the allowed directory
        base_path = os.path.abspath(os.path.dirname(__file__))
        print(base_path)
        requested_path = os.path.abspath(os.path.join(base_path, path[1:]))
        print(requested_path)
        return requested_path.startswith(base_path)
    def send_not_found(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body>404 - Not Found</body></html>")
    def send_forbidden(self):
        self.send_response(403)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body>403 - Forbidden</body></html>")
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    server_address= HOST, PORT
    server = HTTPServer(server_address,requestHandler)
    print("Serving at: http://{}:{}".format(HOST, PORT))
    server.serve_forever()