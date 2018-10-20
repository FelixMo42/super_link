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

def setup(file):
	global var
	global sets
	global sets_count
	global links
	global linkers

	with open("data/" + file + ".json", 'r') as content_file:
		data = json.loads(content_file.read())

	sets = data["vars"]

	for name in data["vars"]:
		links[name] = []
		linkers[name] = []
		sets_count[name] = {}

	id = 0
	for link in data["links"]:
		i = 0
		for v in link["vars"]:
			links[name].append({
				"output": v,
				"func": types[link["name"]][i],
				"id": id,
				"req": link["vars"]
			})
			id += 1
			i += 1

	print(link)

	for v in links:
		for link in links[v]:
			for name in link["req"]:
				linkers[name].append(link)

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

@app.route('/')
def index():
	setup("test")
	dump()
	return render_template("index.html", variables=sets)

@app.route('/', methods=["PATCH"])
def update_var():
	data = json.loads(request.data)

	print("data: ", data)

	if data["value"] == "":
		clear( data["name"] )
		del var[data["name"]]
	else:
		var[data["name"]] = eval(data["value"])
		update( data["name"] )

	dump()

	return json.dumps(sets)

if __name__ == "__main__":
	app.run()
