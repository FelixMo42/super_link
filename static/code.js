const Http = new XMLHttpRequest();
const url = window.location.href

function update(name, value) {
	data = {"name": name, "value": value}

	Http.open("PATCH", url);
	Http.send( JSON.stringify(data) );
	Http.onreadystatechange = (e) => {
		if (Http.responseText == "") {
			return
		}

		data = JSON.parse(Http.responseText)

		console.log(data)

		for (var key in data) {
			console.log(document.getElementById(key))
			document.getElementById(key).value = data[key]
		}
	}
}
