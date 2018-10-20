const Http = new XMLHttpRequest();
const url = window.location.href

sets = []

function clear() {
	for ( var i = 0; i < sets.length; i++ ) {
		console.log(sets[i])
		sets[i].placeholder = ""
	}

	sets = []
}

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

		clear()

		for (var key in data) {
			document.getElementById(key).placeholder = data[key]
			sets.push( document.getElementById(key) )
		}
	}
}
