from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True
@app.route("/")
@app.route("/hello")

def hello_word():
	return "<html><head><title>Page Title</title></head><body><h1>Fang meng qian</h1><p>This is a paragraph.</p></body></html>"
@app.route("/test/<search_query>")
def search(search_query):
	return search_query
@app.route("/<int:value>")

def int_type(value):
	print value + 1
	return "correct"
	
@app.route("/path/<path:value>")
def path_type(value):
	print value
	return "correct"
@app.route("/name/<name>")

def index(name):
	if name.lower() == 'zhenwei':
		return "Hello, {}".format(name), 200
	else:
		return "Not Found", 404
if __name__ == "__main__":
	app.run()