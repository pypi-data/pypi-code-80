from flask import Flask

# the all-important app variable:
app = Flask(__name__)

@app.route("/")
def hello():
    r =  '<html><head><title>It Works!</title></head><body>\n'
    r += '<h2>Hello World from The OICP Team!</h2><br/>\n<br/>\n'
    r += '</body>\n'
    return r

if __name__ == "__main__":
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', debug=True, port=8080)
