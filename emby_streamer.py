'''
    Copyright (C) 2014-2016 ddurdle

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


	This is sample code demonstrating resumable stream of a video file to a browser.

'''


from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import sys
import re
import os



class MyHTTPServer(HTTPServer):

    def __init__(self, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.ready = True




class myStreamer(BaseHTTPRequestHandler):



	#Handler for the GET requests
    def do_GET(self):
        print(self.headers)
        headers = str(self.headers)
        url = str(self.path)
        url = re.sub('8080', '8096', url)

        self.send_response(307)

        self.send_header('Location',url)
        self.end_headers()

server = MyHTTPServer(('', 8080), myStreamer)
while server.ready:
    server.handle_request()
server.socket.close()
sys.exit()

