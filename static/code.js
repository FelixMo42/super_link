const Http = new XMLHttpRequest();
const url = window.location.href

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
		}
	}
}

function newVarCallback() {
	name = this.value

	if (name == "") {
		alert("You must enter a variable name!")
		document.getElementById("varNamer_name").select()
		return
	}

	document.getElementById("variables").innerHTML += name + ": <input id='" + name + "' onchange='update(this.id, this.value)'><br>"
	document.getElementById("varNamer").style.display = "none"

	Http.open("POST", url);
	Http.send( name );
}

function newVar() {
	document.getElementById("varNamer").style.display = "block";
	document.getElementById("varNamer_name").select()
	document.getElementById("varNamer_name").onchange = newVarCallback
}
