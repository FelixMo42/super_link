var Http = new XMLHttpRequest();
const url = window.location.href

//pop up funcs

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

//calc funcs

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

//var funcs

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

		varHTML  = "<span value='" + name + "' oncontextmenu='varMenu(this); return false;'>"
		varHTML += " <span class='varName'>" + name + "</span>: "
		varHTML += " <input id='" + name + "' value='' placeholder='' onchange='update(this.id, this.value)'>"
		varHTML += " <br>"
		varHTML += "</span>"

		document.getElementById("variables").innerHTML += varHTML
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

			el.setAttribute("value", this.value)
		}
	}
}

//link funcs

function newLink(type) {
	showPopup("linkEdit")
	document.getElementById("linkEdit").setAttribute("type", type)
}

function saveLink(el) {
	vars = {}

	for(var child = el.firstChild; child !== null; child = child.nextSibling) {
		if (child.nodeName == "INPUT") {
			vars[child.value] = ""
		}
	}

	data = {"name": document.getElementById("linkEdit").getAttribute("type"), "vars": vars}

	Http.open("NEW_LINK", url);
	Http.send( JSON.stringify(data) );
}

function linkMenu(el) {
	showPopup("linkMenu")

	document.getElementById("linkMenu_delete").onclick = function() {
		el.parentNode.removeChild(el)
		hidePopup("linkMenu")

		Http.open("DELETE_LINK", url);
		Http.send( el.id );

		for(var child = el.firstChild; child !== null; child = child.nextSibling) {
			if (child.nodeName == "SPAN" && document.getElementById(child.innerHTML).value != "") {
				value = document.getElementById(child.innerHTML).value
				update(document.getElementById(child.innerHTML).id, "")
				update(document.getElementById(child.innerHTML).id, value)
				break
			}
		}
	}
	document.getElementById("linkMenu_rename").onclick = function() {
	}
}
