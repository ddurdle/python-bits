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


        print self.headers
        self.send_response(200)
        self.end_headers()

        headers = str(self.headers)
        parameters = re.search(r'direction\=(\S+)', str(self.path))
        if parameters is not None:
            direction = str(parameters.group(1))
            print "direction = " + str(direction) + "\n"
        else:
            return

        if direction == 1:
            os.system('cd /u01/PERL-CloudSync; perl console.pl -c move-testing1')
            self.wfile.write('successful')

        elif direction == 2:
            os.system('cd /u01/PERL-CloudSync; perl console.pl -c move-testing2')
            self.wfile.write('successful')



server = MyHTTPServer(('', 8181), myStreamer)
while server.ready:
    server.handle_request()
server.socket.close()
sys.exit()

