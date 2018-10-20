from flask import Flask, render_template, request
import json

app = Flask("link")

var = {}
link = {}

def update(name):
	if "a" in var and "b" in var:
		return {"c": var["a"] + var["b"]}
	else:
		return {}

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/', methods=["PATCH"])
def update_var():
	data = json.loads(request.data)

	print(data)

	var[data["name"]] = eval(data["value"])

	print( var )
	return json.dumps(update(data["name"]))

if __name__ == "__main__":
    app.run()
