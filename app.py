from flask import Flask, render_template, request
import json

app = Flask("link")

var = {}
sets = {}
links = {
	"c" : [
		{
			"req": ["a", "b"],
			"func": lambda a : a[0] + a[1]
		}
	],
	"b" : [
		{
			"req": ["c", "a"],
			"func": lambda a : a[0] - a[1]
		}
	],
	"a" : [
		{
			"req": ["c", "b"],
			"func": lambda a : a[0] - a[1]
		}
	]
}

def cheak(name, link):
	vars = []
	for v in link["req"]:
		if v in var:
			vars.append(var[v])
		elif v in sets:
			vars.append(sets[v])
		else:
			return


	sets[name] = link["func"](vars)
	#updates[name] = sets[name]

def update():
	for name in links:
		if name not in var:
			for link in links[name]:
				cheak(name, link)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/', methods=["PATCH"])
def update_var():
	global sets

	sets = {}

	data = json.loads(request.data)

	print("data: ", data)

	if data["value"] == "":
		del var[data["name"]]
	else:
		var[data["name"]] = eval(data["value"])

	print( "var: ", var )
	print( "sets: ", sets )

	update()

	return json.dumps(sets)

if __name__ == "__main__":
    app.run()
