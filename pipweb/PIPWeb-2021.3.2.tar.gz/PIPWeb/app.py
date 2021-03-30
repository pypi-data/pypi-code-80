import subprocess
import sys
from flask import Flask, flash, redirect, render_template, url_for, request
import webbrowser

index_html = """<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="{{ url_for('static', filename='js/test.js') }}"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles/dracula.css') }}">
    <script src="{{ url_for('static', filename='js/highlight.pack.js') }}"></script>
    <script>
        hljs.highlightAll();
    </script>
    <title>PIPWeb - Web Python Package Installer, Upgrader & Remover</title>
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">PIPWeb</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/">Home</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container my-3">
        <h2>Install a Package</h2>
        <form action="/install" method="POST">
            <div class="mb-3">
                <label for="package" class="form-label">Package Name</label>
                <input type="text" class="form-control" name="package" id="package" aria-describedby="emailHelp">
            </div>

            <button type="submit" class="btn btn-dark">Submit</button>
        </form>
    </div>

    <div class="container my-3">
        <h2>Upgrade a Package</h2>
        <form action="/upgrade" method="POST">
            <div class="mb-3">
                <label for="package" class="form-label">Package Name</label>
                <input type="text" class="form-control" name="package" id="package" aria-describedby="emailHelp">
            </div>

            <button type="submit" class="btn btn-dark">Submit</button>
        </form>
    </div>

    <div class="container my-3">
        <h2>Remove a Package</h2>
        <form action="/remove" method="POST">
            <div class="mb-3">
                <label for="package" class="form-label">Package Name</label>
                <input type="text" class="form-control" name="package" id="package" aria-describedby="emailHelp">
            </div>

            <button type="submit" class="btn btn-dark">Submit</button>
        </form>
    </div>
    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.6.0/dist/umd/popper.min.js" integrity="sha384-KsvD1yqQ1/1+IA7gi3P0tyJcT3vR+NdBTt13hSJ2lnve8agRGXTTyNaBYmCR/Nwi" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.min.js" integrity="sha384-nsg8ua9HAw1y0W1btsyWgBklPnCUAFLuTMS2G72MMONqmOymq585AcH49TLBQObG" crossorigin="anonymous"></script>
        -->
</body>

</html>
"""

app = Flask(__name__)

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def upgrade(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

def remove(package):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package, "-y"])

@app.route('/', methods=['GET'])
def home():
    return index_html

@app.route('/install', methods=['GET', 'POST'])
def Install():
    if request.method == 'POST':
        package = request.form['package']
        install(package)
        return redirect(url_for('home'))
    else:
        return "Error!"

@app.route('/upgrade', methods=['GET', 'POST'])
def Upgrade():
    if request.method == 'POST':
        package = request.form['package']
        upgrade(package)
        return redirect(url_for('home'))
    else:
        return "Error!"

@app.route('/remove', methods=['GET', 'POST'])
def Remove():
    if request.method == 'POST':
        package = request.form['package']
        remove(package)
        return redirect(url_for('home'))
    else:
        return "Error!"

def main():

    def init():
        install("flask")

    init = init()
        
    def run():
        url = "http://localhost:9999"
        webbrowser.open_new_tab(url)
        app.run(host='0.0.0.0', port=9999)

    run = run()