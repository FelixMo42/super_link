from flask import Flask, render_template, request
import json

app = Flask("link")

var = {}
sets = {}
sets_count = {}
links = {}
linkers = {}

types = {
	"add":  lambda a : a[0] + a[1]
}

def setup(file):
	global var
	global sets
	global sets_count
	global links
	global linkers

	with open("data/" + file, 'r') as content_file:
		data = json.loads(content_file.read())

	sets = data["vars"]

	for name in data["vars"]:
		links[name] = []
		linkers[name] = []
		sets_count[name] = {}

	id = 0
	for name in data["links"]:
		for t in data["links"][name]:
			links[name].append({
				"output": name,
				"func": types[t],
				"id": id,
				"req": data["links"][name][t]
			})

	for v in links:
		for link in links[v]:
			for name in link["req"]:
				linkers[name].append(link)

def cheak(link, clear=False):
	vars = []
	for v in link["req"]:
		if v in var:
			vars.append(var[v])
		elif v in sets and sets[v] != "":
			vars.append(sets[v])
		else:
			return

	if link["output"] in sets:
		if clear:
			del sets_count[link["output"]][link["id"]]
			if len(sets_count[link["output"]]) == 0:
				sets[link["output"]] = ""
		else:
			sets[link["output"]] = link["func"](vars)
			sets_count[link["output"]][link["id"]] = True
	else:
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
	'''global var
	global sets
	global sets_count

	var = {}
	sets = {}
	sets_count = {}'''

	#setup("test.json")

	return render_template("index.html", variables=sets)

@app.route('/', methods=["PATCH"])
def update_var():
	data = json.loads(request.data)

	print("data: ", data)

	print(var)

	if data["value"] == "":
		clear( data["name"] )
		del var[data["name"]]
	else:
		var[data["name"]] = eval(data["value"])
		update( data["name"] )

	print( "var: ", var )
	print( "sets: ", sets )
	print( "sets_count: ", sets_count )

	return json.dumps(sets)

if __name__ == "__main__":
	setup("test.json")
	app.run()
