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

    def setDomain(self, domain):
        self.domain = domain
        self.ready = True


class myStreamer(BaseHTTPRequestHandler):




	#Handler for the POST requests
	def do_GET(self):
		print(self.headers)
		headers = str(self.headers)

		#content_len = int(self.headers.getheader('content-length', 0))
		#post_body = self.rfile.read(content_len)

		print 'http:/' + str(self.server.domain) + str(self.path)

#		for r in re.finditer('redirect\=(.*)' ,
#				     post_body, re.DOTALL):
#		  redirect = r.group(1)
#		  print "ib ib" + post_body
#		  print "\n\n" + redirect
#		  break
		self.server.ready = False
		return

server = MyHTTPServer(('', 8094), myStreamer)
server.setDomain('4.bp.blogspot.com')
while server.ready:
    server.handle_request()
server.socket.close()
sys.exit()

