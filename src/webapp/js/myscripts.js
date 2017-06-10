function updatePhoto(event){
	var reader = new FileReader()
	reader.onload = function(event){
		//Create img
		var img = new Image();
		img.onload = function(){
			//Place img on screen
			canvas = document.getElementById("photo");
			ctx = canvas.getContext("2d");
			ctx.drawImage(img,0,0,img.width,img.height,0,0,640,480);
		}
		img.src = event.target.result;
	}
	//Get File
	reader.readAsDataURL(event.target.files[0]);
	sendFile(event.target.files[0]);
	
	window.URL.revokeObjectURL(picURL);
}

function sendFile(file) {
	var data = new FormData();
	data.append("image", file);
	data.append("type", "EFFECT")
	data.append("effect", "sepia")
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "put");
	xhr.upload.addEventListener("progress", updateProgress, false);
	xhr.send(data);

}

function updateProgress(evt){
	if(evt.loaded == evt.total)
		alert("Ok");
}
