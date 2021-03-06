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

        useragent = re.search(r'User-Agent\: (\S+)', str(self.headers))
        if useragent is not None:
            useragent = str(useragent.group(1))
            header = { 'User-Agent' : useragent}

        print self.headers
        self.send_response(200)
        self.end_headers()

        headers = str(self.headers)
        url = re.search(r'path\=(\S+)', str(self.path))
        if url is not None:
            url = str(url.group(1))
            print "URL = " + str(url) + "\n"
        else:
            return
        retry = 1
        while(retry and retry < 10):
            print url + "\n"

            req = urllib2.Request(url, None,header)
            try:
                response = urllib2.urlopen(req)
                retry = 0
            except urllib2.URLError, e:
                print str(e)
                retry += 1

        chunksize = 24*512*1024
        if retry == 0:
            while True:
                print "reading...\n"
                chunk = response.read(chunksize)
                if len(chunk) == 0:
                    break
                self.wfile.write(chunk)


            #response_data = response.read()
            #response_data = str(re.sub('/hlsr/', 'http://uslb01.warriorsiptv.com:8880/hlsr/', response_data))
            #self.wfile.write(response_data)

            #response_data = response.read()
            response.close()


server = MyHTTPServer(('', 8080), myStreamer)
while server.ready:
    server.handle_request()
server.socket.close()
sys.exit()

