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
            else:
                self.send_not_found()
        else:
            self.send_forbidden()
        """
        This method is responsible for handling an http-request. You can, and should(!),
        make additional methods to organize the flow with which a request is handled by
        this method. But it all starts here!
        """
    def do_POST(self):
        if self.is_safe_path(self.path):
            if self.path.endswith('test.txt'):
                try:
                    # Parse the content type header
                    ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
                    print(ctype, pdict)
                    # Check if the content type is 'application/x-www-form-urlencoded'
                    if ctype == 'application/x-www-form-urlencoded':
                        # Read the content length
                        content_length = int(self.headers.get('Content-Length'))

                        # Parse the form data
                        form_data = self.rfile.read(content_length).decode('utf-8')
                        print(form_data)
                        # Parse the form data into a dictionary
                        fields = cgi.parse_qs(form_data)

                        # Get the 'input_text' field value
                        new_input = fields.get('input_text', [''])[0]

                        # Append the input to the global input_list
                        input_list.append(new_input)

                        # Send a 301 redirect response
                        self.send_response(301)
                        self.send_header('Content-Type', 'text/html')
                        self.send_header('Location', '/index.html')
                        self.end_headers()
                    else:
                        # Handle other content types if needed
                        self.send_error(400, "Bad Request: Unsupported Content-Type")
                except Exception as e:
                    # Handle exceptions
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
        requested_path = os.path.abspath(os.path.join(base_path, path[1:]))
        return requested_path.startswith(base_path)
    def send_not_found(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "9")
        self.end_headers()
        self.wfile.write(b"Not Found")
    def send_forbidden(self):
        self.send_response(403)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "9")
        self.end_headers()
        self.wfile.write(b"Forbidden")
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    server_address= HOST, PORT

    server = HTTPServer(server_address,requestHandler)
    print("Serving at: http://{}:{}".format(HOST, PORT))
    server.serve_forever()
