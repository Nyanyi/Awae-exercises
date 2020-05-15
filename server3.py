import http.server as SimpleHTTPServer
import socketserver as SocketServer
import sys
from  urllib import parse

port = int(sys.argv[1])

class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		parsed_path = parse.urlparse(self.path)
		message_parts = [
            	'CLIENT VALUES:',
            	'>client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            	'>command={}'.format(self.command),
            	'>path={}'.format(self.path),
            	'>real path={}'.format(parsed_path.path),
            	'>query={}'.format(parsed_path.query),
            	'>request_version={}'.format(self.request_version),
		'',
           	'HEADERS RECEIVED:',
        	]
		for name, value in sorted(self.headers.items()):
			message_parts.append(
				'>{}={}'.format(name, value.rstrip())
			)
		message_parts.append('')
		message = '\r\n'.join(message_parts)
		print(message)

		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)




Handler = GetHandler
with SocketServer.TCPServer(("", port), Handler) as httpd:
	print ("Starting server at port", port)
	httpd.serve_forever()
