from flask import Flask, render_template, request
import json

app = Flask("link")

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/', methods=["PATCH"])
def update_var():
	data = json.loads(request.data)
	return data["value"]

if __name__ == "__main__":
    app.run()