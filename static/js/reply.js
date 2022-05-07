function showReplyForm(id) {
	console.log(id)
	var object = document.getElementById(id)

	if (object.classList.contains('d-none')) {
		object.classList.remove('d-none')
	} else {
		object.classList.add('d-none')
	}
}


console.log("Wait what")