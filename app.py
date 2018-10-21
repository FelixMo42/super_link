from flask import Flask, render_template, request, Markup
import json

id = 0

app = Flask("link")

var = {}
sets = {}
sets_count = {}
links = {}
linkers = {}

types = {
	"add": [
		lambda a : a[2] - a[1],
		lambda a : a[2] - a[0],
		lambda a : a[0] + a[1],
		"%s + %s = %s"
	],
	"subtract": [
		lambda a : a[2] + a[1],
		lambda a : a[2] + a[0],
		lambda a : a[0] - a[1],
		"%s - %s = %s"
	],
	"multiply": [
		lambda a : a[2] / a[1],
		lambda a : a[2] / a[0],
		lambda a : a[0] * a[1],
		"%s * %s = %s"
	],
	"divide": [
		lambda a : a[2] * a[1],
		lambda a : a[2] * a[0],
		lambda a : a[0] / a[1],
		"%s / %s = %s"
	]
}

for t in types:
	types[t][-1] = Markup(types[t][-1].replace("%s", "<span class=''>%s</span>"))

def dump():
	print("var: ", var)
	print("sets: ", sets)
	print("sets_count: ", sets_count)
	#print("links: ", links)
	#print("linkers: ", linkers)

#var funcs

def addVar(name):
	global sets
	global sets_count
	global linkers

	sets[name] = ""
	sets_count[name] = {}
	linkers[name] = []

def delVar(name):
	global vars
	global sets
	global sets_count
	global linkers

	if name in var:
		del var[name]
	if name in sets:
		del sets[name]
	if name in sets_count:
		del sets_count[name]
	if name in linkers:
		del linkers[name]

#link funcs

def addLink(link,cid=id):
	global id
	global links
	global linkers

	i = 0

	for name in link["vars"]:
		for target in link["vars"]:
			if name != target:
				linkers[target].append({
					"output": name,
					"func": types[link["name"]][i],
					"cid": cid,
					"req": link["vars"],
					"name": link["name"]
				})
		i += 1

	id += 1

	links[cid] = link

	return cid

def delLink(cid):
	global links
	global linkers

	link = links[cid]

	for name in link["vars"]:
		clear(name)
		i = 0
		print(linkers)
		while i < len(linkers[name]):
			#print(i)
			if linkers[name][i]["cid"] == cid:
				del linkers[name][i]
			else:
				i += 1

	del links[cid]

#manager funcs

def reset():
	global vars
	global sets
	global sets_count
	global links
	global linkers

	var = {}
	sets = {}
	sets_count = {}
	links = {}
	linkers = {}

def setup(file):
	global id
	global var
	global links
	global linkers

	reset()

	with open("data/" + file + ".json", 'r') as load_file:
		data = json.loads(load_file.read())

	id = data["id"]

	for name in data["vars"]:
		addVar(name)
		if data["vars"][name] != "":
			var[name] = data["vars"][name]

	for cid in data["links"]:
		addLink(data["links"][cid], cid)

	for name in var:
		update(name)

def save(file):
	data = {"vars": {}, "links": {}, "id": id}

	for v in sets:
		data["vars"][v] = ""

	for v in var:
		data["vars"][v] = var[v]

	for cid in links:
		data["links"][str(cid)] = links[cid]

	with open("data/" + file + ".json", "w") as save_file:
		save_file.write(json.dumps(data))

#update the maths

def cheak(link, empty=False):
	vars = []
	for v in link["req"]:
		if v == link["output"]:
			vars.append(False)
		elif v in var:
			vars.append(var[v])
		elif v in sets and sets[v] != "":
			vars.append(sets[v])
		else:
			return

	if link["output"] in sets and sets[link["output"]] != "":
		if empty:
			del sets_count[link["output"]][link["cid"]]
			if len(sets_count[link["output"]]) == 0:
				clear(link["output"])
				sets[link["output"]] = ""
		else:
			sets[link["output"]] = link["func"](vars)
			sets_count[link["output"]][link["cid"]] = True
	elif not empty:
		sets[link["output"]] = link["func"](vars)
		sets_count[link["output"]] = {link["cid"]: True}
		update(link["output"])

def update(name):
	for link in linkers[name]:
		if link["output"] not in var:
			cheak(link)

def clear(name):
	for link in linkers[name]:
		cheak(link, True)

#flask functions

@app.route('/')
def index():
	save("test")
	setup("test")
	dump()
	return render_template("index.html", variables=sets, value=var, sets=sets, links=links, types=types, list=list, tuple=tuple)

@app.route('/', methods=["SET_VAR"])
def set_var():
	data = json.loads(request.data)

	print("data: ", data)

	if data["value"] == "":
		print("clear")
		#clear( data["name"] )
		del var[data["name"]]
		save("test")
		setup("test")
	else:
		try:
			var[data["name"]] = eval(data["value"])
		except:
			print("THERE WAS AN ERROR")
			#clear( data["name"] )
			save("test")
			setup("test")
			return "Must be a number or Python3 code resulting in a number" + "\n" + json.dumps(sets)

		#update( data["name"] )
		save("test")
		setup("test")

	return json.dumps(sets)

@app.route('/', methods=["NEW_VAR"])
def new_var():
	addVar(request.data.decode("utf8"))
	save("test")
	return ""

@app.route('/', methods=["DELETE_VAR"])
def delete_var():
	delVar(request.data.decode("utf8"))
	save("test")
	return ""

@app.route('/', methods=["RENAME_VAR"])
def rename_var():
	print(request.data)
	data = json.loads(request.data)

	for key in var:
		if key == data["old"]:
			var[data["new"]] = var[data["old"]]
			del var[data["old"]]

	for key in sets:
		if key == data["old"]:
			sets[data["new"]] = sets[data["old"]]
			del sets[data["old"]]

	for key in sets_count:
		if key == data["old"]:
			sets_count[data["new"]] = sets_count[data["old"]]
			del sets_count[data["old"]]

	for key in linkers:
		for link in linkers[key]:
			if link["output"] == data["old"]:
				link["output"] = data["new"]
			link["req"] = [data["new"] if name == data["old"] else name for name in link["req"]]

		if key == data["old"]:
			linkers[data["new"]] = linkers[data["old"]]
			del linkers[data["old"]]

	dump()
	save("test")
	pass

@app.route('/', methods=["NEW_LINK"])
def new_link():
	print(request.data)
	cid = addLink(json.loads(request.data))
	save("test")
	return "<span class='link' id='" + links[cid]["name"] + "' oncontextmenu='linkMenu(this); return false;'>" + types[links[cid]["name"]][-1] % tuple(list(links[cid]["vars"])) + "<br></span>"

@app.route('/', methods=["DELETE_LINK"])
def delete_link():
	delLink(request.data.decode("utf8"))
	save("test")
	return ""

@app.route('/', methods=["EDIT_LINK"])
def edit_link():
	data = json.loads(request.data)
	link = link[data["cid"]]

	for key in link["vars"]:
		del link["vars"][key]
	for key in data["vars"]:
		link["vars"][key] = data["vars"]

	save("test")
	return ""

if __name__ == "__main__":
	setup("test")
	app.run()
