from flask import Flask, render_template, request
import json

app = Flask("link")

var = {}
sets = {}
sets_count = {}

links = {
	"c" : [
		{
			"output": "c",
			"req": ["a", "b"],
			"func": lambda a : a[0] + a[1]
		}
	],
	"b" : [
		{
			"output": "b",
			"req": ["c", "a"],
			"func": lambda a : a[0] - a[1]
		}
	],
	"a" : [
		{
			"output": "a",
			"req": ["c", "b"],
			"func": lambda a : a[0] - a[1]
		}
	]
}
linkers = {}

def setup():
	for var in links:
		for link in links[var]:
			for name in link["req"]:
				if name not in linkers:
					linkers[name] = []
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
			sets_count[link["output"]] = sets_count[link["output"]] - 1
			if sets_count[link["output"]] == 0:
				sets[link["output"]] = ""
		else:
			sets_count[link["output"]] = sets_count[link["output"]] + 1
	else:
		sets[link["output"]] = link["func"](vars)
		sets_count[link["output"]] = 1

def update(name):
	for link in linkers[name]:
		if link["output"] not in var:
			cheak(link)

def clear(name):
	for link in linkers[name]:
		cheak(link, True)

@app.route('/')
def index():
	global var
	global sets
	global sets_count

	var = {}
	sets = {}
	sets_count = {}

	return render_template("index.html")

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

	print( "var: ", var )
	print( "sets: ", sets )
	print( "sets_count: ", sets_count )

	return json.dumps(sets)

if __name__ == "__main__":
	setup()
	app.run()
