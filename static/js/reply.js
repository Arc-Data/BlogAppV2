function showReplyForm(id) {
	var object = document.getElementById(id)


	if(object.classList.contains('d-none')) {
		object.classList.remove('d-none')
	} else {
		object.classList.add('d-none')
	}
}



