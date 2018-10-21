var Http = new XMLHttpRequest();
const url = window.location.href

function showPopup(popup) {
	document.getElementById("shade").style.display = "block";
	document.getElementById(popup).style.display = "block";

	document.getElementById("shade").onclick = function() {
		hidePopup(popup)
	}
}

function hidePopup(popup) {
	document.getElementById("shade").style.display = "none";
	document.getElementById(popup).style.display = "none";
}

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
	showPopup("varNamer")
	document.getElementById("varNamer_name").select()
	document.getElementById("varNamer_name").onchange = function() {
		name = this.value

		if (name.replace(/\s+/g, '') == "") {
			alert("You must enter a variable name!")
			document.getElementById("varNamer_name").select()
			return
		}

		if (document.getElementById(name)) {
			alert("Name is allready taken!")
			document.getElementById("varNamer_name").select()
			return
		}

		document.getElementById("variables").innerHTML += name + ": <input id='" + name + "' onchange='update(this.id, this.value)'><br>"
		hidePopup("varNamer")

		Http.open("NEW_VAR", url);
		Http.send( name );
	}
}

function varMenu(el) {
	showPopup("varMenu")
	document.getElementById("varMenu_delete").onclick = function() {
		el.parentNode.removeChild(el)
		hidePopup("varMenu")

		Http.open("DELETE_VAR", url);
		Http.send( el.getAttribute("value") );
	}
	document.getElementById("varMenu_rename").onclick = function() {
		hidePopup("varMenu")
		showPopup("varNamer")
		document.getElementById("varNamer_name").select()
		document.getElementById("varNamer_name").onchange = function() {
			if (this.value.replace(/\s+/g, '') == "") {
				alert("You must enter a variable name!")
				document.getElementById("varNamer_name").select()
				return
			}

			if (document.getElementById(name)) {
				alert("Name is allready taken!")
				document.getElementById("varNamer_name").select()
				return
			}

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
