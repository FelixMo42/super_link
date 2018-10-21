from flask import Flask, render_template, request
import json

app = Flask("link")

var = {}
sets = {}
sets_count = {}
links = {}
linkers = {}

types = {
	"add":  [
		lambda a : a[2] - a[1], #0
		lambda a : a[2] - a[0], #1
		lambda a : a[0] + a[1] #2
	],
	"subtract":  [
		lambda a : a[2] + a[1],
		lambda a : a[2] + a[0],
		lambda a : a[0] - a[1]
	],
	"multiply":  [
		lambda a : a[2] / a[1],
		lambda a : a[2] / a[0],
		lambda a : a[0] * a[1]
	],
	"divide":  [
		lambda a : a[2] * a[1],
		lambda a : a[2] * a[0],
		lambda a : a[0] / a[1]
	]
}

def dump():
	print("var: ", var)
	print("sets: ", sets)
	print("sets_count: ", sets_count)
	#print("links: ", links)
	#print("linkers: ", linkers)

def addVar(name):
	global sets
	global sets_count
	global links
	global linkers

	sets[name] = ""
	sets_count[name] = {}
	links[name] = []
	linkers[name] = []

def delVar(name):
	global vars
	global sets
	global sets_count
	global links
	global linkers

	if name in var:
		print("sets")
		del var[name]
	if name in sets:
		print("sets")
		del sets[name]
	if name in sets_count:
		print("sets_count")
		del sets_count[name]
	if name in links:
		print("links")
		print(links[name])
		del links[name]
	if name in linkers:
		print("linkers")
		del linkers[name]

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
	global var
	global links
	global linkers

	reset()

	with open("data/" + file + ".json", 'r') as load_file:
		data = json.loads(load_file.read())

	for name in data["vars"]:
		addVar(name)
		if data["vars"][name] != "":
			var[name] = data["vars"][name]

	id = 0
	for link in data["links"]:
		i = 0
		for v in link["vars"]:
			#if v == v:
			links[v].append({
				"output": v,
				"func": types[link["name"]][i],
				"id": id,
				"cid": id - i,
				"req": link["vars"],
				"name": link["name"]
			})
			id += 1
			i += 1

	for v in links:
		for link in links[v]:
			for name in link["req"]:
				linkers[name].append(link)

	for name in var:
		update(name)

def cheak(link, clear=False):
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
		if clear:
			del sets_count[link["output"]][link["id"]]
			if len(sets_count[link["output"]]) == 0:
				sets[link["output"]] = ""
		else:
			sets[link["output"]] = link["func"](vars)
			sets_count[link["output"]][link["id"]] = True
	elif not clear:
		sets[link["output"]] = link["func"](vars)
		sets_count[link["output"]] = {link["id"]: True}

def update(name):
	for link in linkers[name]:
		if link["output"] not in var:
			cheak(link)

def clear(name):
	for link in linkers[name]:
		cheak(link, True)

def save(file):
	data = {"vars": {}, "links": []}

	for v in sets:
		data["vars"][v] = ""
	for v in var:
		data["vars"][v] = var[v]

	saved = []

	for k in links:
		for l in links[k]:
			if l["cid"] not in saved:
				data["links"].append( {
					"name" : l["name"],
					"vars" : l["req"]
				} )
				saved.append(l["cid"])

	with open("data/" + file + ".json", "w") as save_file:
		save_file.write(json.dumps(data))

@app.route('/')
def index():
	save("test")
	setup("test")
	dump()
	return render_template("index.html", variables=sets, value=var, sets=sets)

@app.route('/', methods=["SET_VAR"])
def set_var():
	data = json.loads(request.data)

	print("data: ", data)

	if data["value"] == "":
		clear( data["name"] )
		del var[data["name"]]
	else:
		try:
			var[data["name"]] = eval(data["value"])
		except:
			print("THERE WAS AN ERROR")
			clear( data["name"] )
			return "Must be a number or Python3 code resulting in a number" + "\n" + json.dumps(sets)

		update( data["name"] )

	dump()

	return json.dumps(sets)

@app.route('/', methods=["NEW_VAR"])
def new_var():
	addVar(request.data.decode("utf8"))
	save("test")
	return ""

@app.route('/', methods=["DELETE_VAR"])
def delete_var():
	print("-" + request.data.decode("utf8") + "-")
	delVar(request.data.decode("utf8"))
	dump()
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

	'''for key in links:
		if key == data["old"]:
			links[data["new"]] = links[data["old"]]
			for link in links[data["new"]]:
				if
			del links[data["old"]]'''

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

if __name__ == "__main__":
	setup("test")
	app.run()
