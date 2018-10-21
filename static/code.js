var Http = new XMLHttpRequest();
const url = window.location.href

function update(name, value) {
	data = {"name": name, "value": value}

	Http.open("SET_VAR", url);
	Http.send( JSON.stringify(data) );
	Http.onreadystatechange = (e) => {
		console.log(Http.responseText)
		console.log(Http.readyState)
		if (Http.responseText == "" || Http.readyState != 4) {
			return
		}

		try {
			document.getElementById(name).classList.remove("wrong")

			data = JSON.parse(Http.responseText)
		} catch(error) {
			document.getElementById(name).classList.add("wrong")

			response = Http.responseText.split("\n")
			alert(response[0])
			data = JSON.parse(response[1])
		}

		console.log(data)

		for (var key in data) {
			document.getElementById(key).placeholder = data[key]
		}
	}
}

function newVar() {
	document.getElementById("varNamer").style.display = "block";
	document.getElementById("varNamer_name").select()
	document.getElementById("varNamer_name").onchange = function() {
		name = this.value

		if (name == "") {
			alert("You must enter a variable name!")
			document.getElementById("varNamer_name").select()
			return
		}

		document.getElementById("variables").innerHTML += name + ": <input id='" + name + "' onchange='update(this.id, this.value)'><br>"
		document.getElementById("varNamer").style.display = "none"

		Http.open("NEW_VAR", url);
		Http.send( name );
	}
}

function varMenu(el) {
	document.getElementById("varMenu").style.display = "block";
	document.getElementById("varMenu_delete").onclick = function() {
		el.parentNode.removeChild(el)
		document.getElementById("varMenu").style.display = "none";

		Http.open("DELETE_VAR", url);
		Http.send( el.id );
	}
	document.getElementById("varMenu_rename").onclick = function() {
		document.getElementById("varMenu").style.display = "none";
		document.getElementById("varNamer").style.display = "block";
		document.getElementById("varNamer_name").select()
		document.getElementById("varNamer_name").onchange = function() {
			Http.open("RENAME_VAR", url);
			Http.send(JSON.stringify({"old": el.getAttribute("value"), "new": this.value}));

			console.log(el.getAttribute("value"))
			console.log(JSON.stringify({"old": el.getAttribute("value"), "new": this.value}))

			for(var child = el.firstChild; child !== null; child = child.nextSibling) {
				console.log(child)
				if (child.nodeName == "SPAN") {
					child.innerHTML = this.value
				} else if (child.nodeName == "INPUT") {
					child.id = this.value
				}
			}
		}
	}
}
