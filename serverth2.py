from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from sys import argv
from  urllib import parse
import threading
import time

#use: serverth2.py port

#Server port assignment
port = int(argv[1])

#inheritance of SimpleHTTPServer
class Handler(SimpleHTTPRequestHandler):
	def do_GET(self):
		global control
		parsed_path = parse.urlparse(self.path)
		message_parts = [
            	'CLIENT VALUES:',
            	'>client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            	'>command={}'.format(self.command),
            	'>path={}'.format(self.path),
            	'>real path={}'.format(parsed_path.path),
            	'>query=>{}'.format(parsed_path.query),
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
		cookie= parsed_path.query
		print(cookie)
		if(cookie):
			print("Bye, your cookie is", cookie)
			# server down
			thread2.start()

		SimpleHTTPRequestHandler.do_GET(self)


#main

server= TCPServer(("", port), Handler)
print("Start")
thread=threading.Thread(target=server.serve_forever)
thread.start()
thread2=threading.Thread(target=server.shutdown)

