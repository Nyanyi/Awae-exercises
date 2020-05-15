import http.server as SimpleHTTPServer
import socketserver as SocketServer
import logging
import sys
from  urllib import parse

port = int(sys.argv[1])

class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		parsed_path = parse.urlparse(self.path)
		query = parsed_path.query
		print(query)
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)




Handler = GetHandler
with SocketServer.TCPServer(("", port), Handler) as httpd:
	print ("Starting server at port", port)
	httpd.serve_forever()
