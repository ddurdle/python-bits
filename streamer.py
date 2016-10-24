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

    def setFile(self, playbackURL, chunksize, playbackFile, response, size):
		self.playbackURL = playbackURL
		self.chunksize = chunksize
		self.playbackFile = playbackFile
		self.response = response
		self.size = size
		self.ready = True
		self.state = 0


class myStreamer(BaseHTTPRequestHandler):



	#Handler for the GET requests
	def do_GET(self):
		print(self.headers)
		headers = str(self.headers)
		url = str(self.path)
		print "url = " + url + "\n"
		start = ''
		end = 0
		count = 0
		for r in re.finditer('Range\:\s+bytes\=(\d+)\-' ,
				     headers, re.DOTALL):
		  start = int(r.group(1))
		  break
		for r in re.finditer('Range\:\s+bytes\=\d+\-(\d+)' ,
				     headers, re.DOTALL):
		  end = int(r.group(1))
		  break

		if start == '':
			self.send_response(200)
			self.send_header('Content-Length',self.server.size)
		else:
			self.send_response(206)
			if start  > 0:
				count = int(start/int(self.server.chunksize))

			self.send_header('Content-Length',str(self.server.size-(count*int(self.server.chunksize))))
			self.send_header('Content-Range','bytes ' + str(start) + '-' + str(self.server.size-1)+'/'+str(self.server.size))

		self.send_header('Content-type','video/mp4')

		self.send_header('Accept-Ranges','bytes')
		self.end_headers()
		if self.server.state != 0:

			#fi = open(self.server.playbackFile, 'ab')
			#self.server.state = 1
			while True:

				with open(self.server.playbackURL, "rb") as f:
					f.seek(self.server.chunksize*count,0)
					chunk = f.read(self.server.chunksize)
					self.wfile.write(chunk)
					print "sending chunk " + str(count)   + "\n"
				f.close()
				if not chunk: break
				count = count + 1

			#fi.close()


			#except: pass
			#self.server.ready = False

		else:

			self.server.state = 1
			self.server.ready = True

		return

CHUNK = 4096*100
file = '/u01/test.ogv'
server = MyHTTPServer(('', 8094), myStreamer)
server.setFile(file,CHUNK, '', '', os.path.getsize(file))
while server.ready:
    server.handle_request()
server.socket.close()
sys.exit()

