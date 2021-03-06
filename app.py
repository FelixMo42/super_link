from flask import Flask, render_template, request, Markup
from os import listdir
import json

uid = 0
loc = "do_not_save_here!_this_is_for_real_time_data!23b87x4r287"

app = Flask('app')

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
	],#
	"temp_CeFa": [
		lambda a : (a[1] * 5/9.0) + 32,
		lambda a : (a[0] * 9/5.0) + 32,
		"%s°C = %s°F"
	],
	"dist_MiKi": [
		lambda a : a[1] * 0.62137119,
		lambda a : a[0] / 0.62137119,
		"%sMi = %sKm"
	]
}

for t in types:
	types[t][-1] = Markup(types[t][-1].replace("%s", "<span class=''>%s</span>"))

##

def dump():
	print("var: ", var)
	print("sets: ", sets)
	print("sets_count: ", sets_count)
	print("links: ", links)
	print("linkers: ", linkers)

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

def addLink(link, cid=False):
	global uid
	global links
	global linkers

	i = 0

	if not cid:
		cid = uid
		uid += 1

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

	links[cid] = link

	return cid

def delLink(cid):
	global links
	global linkers

	save(loc)
	setup(loc)

	del links[cid]

	save(loc)
	setup(loc)

	'''for name in link["vars"]:
		clear(name)
		i = 0
		print(linkers)
		while i < len(linkers[name]):
			if linkers[name][i]["cid"] == cid:
				del linkers[name][i]
			else:
				i += 1'''

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
	global uid
	global var
	global links
	global linkers

	reset()

	with open("data/" + file + ".json", 'r') as load_file:
		data = json.loads(load_file.read())
		print(data)

	uid = data["id"]

	for name in data["vars"]:
		addVar(name)
		if data["vars"][name] != "":
			var[name] = data["vars"][name]

	for cid in data["links"]:
		addLink(data["links"][cid], cid)

	for name in var:
		update(name)

def save(file):
	data = {"vars": {}, "links": {}, "id": uid}

	for v in sets:
		data["vars"][v] = ""

	for v in var:
		data["vars"][v] = var[v]

	for cid in links:
		data["links"][str(cid)] = links[cid]

	with open("data/" + file + ".json", "w") as save_file:
		save_file.write(json.dumps(data))

##

@app.route('/')
def index():
	save(loc)
	setup(loc)
	return render_template("index.html",
		variables=sets, value=var, sets=sets,
		links=links, types=types, files=listdir("data"),
		list=list, tuple=tuple,
	)

@app.route('/help')
def load_help():
	return render_template("help.html")

@app.route('/about')
def load_about():
	return render_template("about.html")

@app.route('/doc')
def doc():
	return render_template("doc.html")

@app.route('/', methods=["SET_VAR"])
def set_var():
	if request.data != "":
		data = json.loads(request.data)

		print("data: ", data)

		if data["value"] == "":
			print("clear")
			#clear( data["name"] )
			del var[data["name"]]
			save(loc)
			setup(loc)
		else:
			try:
				var[data["name"]] = eval(data["value"])

				save(loc)
				setup(loc)
			except:
				return "Must be a number or Python3 code resulting in a number"


	return json.dumps(sets)

@app.route('/', methods=["NEW_VAR"])
def new_var():
	addVar(request.data.decode("utf8"))
	save(loc)
	return ""

@app.route('/', methods=["DELETE_VAR"])
def delete_var():
	delVar(request.data.decode("utf8"))
	save(loc)
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
	save(loc)
	return ""

@app.route('/', methods=["NEW_LINK"])
def new_link():
	print(request.data)
	cid = addLink(json.loads(request.data))
	save(loc)

	dump()

	type="{{links[name]['name']}}"

	html  = '<span class="link" id="' + str(cid) + '" type="' + links[cid]['name'] + '"'
	html += 'oncontextmenu="linkMenu(this); return false;">'
	html += types[links[cid]['name']][-1] % tuple(list(links[cid]['vars'])) + '<br></span>'

	return  html

@app.route('/', methods=["DELETE_LINK"])
def delete_link():
	delLink(request.data.decode("utf8"))
	save(loc)
	return ""

@app.route('/', methods=["EDIT_LINK"])
def edit_link():
	data = json.loads(request.data)
	link = link[data["cid"]]

	for key in link["vars"]:
		del link["vars"][key]
	for key in data["vars"]:
		link["vars"][key] = data["vars"]

	save(loc)
	return ""

@app.route('/', methods=["DATA_SAVE"])
def data_save():
	save(request.data.decode("utf8"))

	return ""

@app.route('/', methods=["DATA_LOAD"])
def data_load():
	print(request.data.decode("utf8"))
	setup(request.data.decode("utf8"))
	save(loc)

	return ""

app.run(host='0.0.0.0', port=8080)
