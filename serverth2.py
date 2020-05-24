from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from sys import argv
from  urllib import parse
import threading
import time




#Server port assignment
port = int(argv[1])
control=0
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
			printer()
			thread2.start()
			#control = 1
			#print("Se ha activado control con el valor", control)
		

		SimpleHTTPRequestHandler.do_GET(self)

server= TCPServer(("", port), Handler)
print("Empezamos")

thread=threading.Thread(target=server.serve_forever)


#def fin():
#	print("bye bye bye")
#	server.shutdown()

#thread2=threading.Thread(target=server.shutdown)
#thread.daemon=True
thread.start()
print("estamos")
def printer():
	print(port)

printer()
thread2=threading.Thread(target=server.shutdown)

#print("Empezando la cuenta atras")
#time.sleep(120)
#thread2.start()

