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
import urllib2



class MyHTTPServer(HTTPServer):

    def __init__(self, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.ready = True




class myStreamer(BaseHTTPRequestHandler):



	#Handler for the GET requests
    def do_GET(self):
        print(self.headers)
        self.send_response(200)
        self.end_headers()

        headers = str(self.headers)
        url = re.search(r'path\=(\S+)', str(self.path))
        if url is not None:
            url = str(url.group(1))

        else:
            print "no url provided\n"
            return
        retry = 1
        while(retry and retry < 10):
            print url + "\n"

            req = urllib2.Request(url)
            try:
                response = urllib2.urlopen(req)
                retry = 0
            except urllib2.URLError, e:
                retry += 1

        if retry == 0:
            self.wfile.write(response.read())

            #response_data = response.read()
            response.close()


server = MyHTTPServer(('', 8080), myStreamer)
while server.ready:
    server.handle_request()
server.socket.close()
sys.exit()

