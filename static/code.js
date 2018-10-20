const Http = new XMLHttpRequest();
const url = window.location.href

sets = []

function update(name, value) {
	data = {"name": name, "value": value}

	Http.open("PATCH", url);
	Http.send( JSON.stringify(data) );
	Http.onreadystatechange = (e) => {
		console.log(Http.responseText)
		if (Http.responseText == "") {
			return
		}

		data = JSON.parse(Http.responseText)

		console.log(data)

		for (var key in data) {
			document.getElementById(key).placeholder = data[key]
			sets.push( document.getElementById(key) )
		}
	}
}
