# python-examples
Examples for use in tutoring a python class

## First steps

Install required Python packages
1. In your terminal, change path (`cd`) to this project's directory
2. Run `pip install -r requirements.txt`
	* *If `pip` doesn't work, try `pip3`*

> Some red warnings may appear. Ignore these, unless you experience errors when running scripts.

## Flask Web Server

1. `cd` to this project's directory
2. export environment variables
    * Linux
        * `export FLASK_ENV=development`
        * `export FLASK_APP=server.py`
    * Windows (PowerShell or Windows Terminal)
        * `$env:FLASK_APP = "server.py"`
        * `$env:FLASK_ENV = "development"`
    * Windows (CMD)
        * `set FLASK_APP=server.py`
        * `set FLASK_ENV=development`
3. Run `flask run`
    * Or `python -m flask run`
    * *Some platforms may use `python3` instead*

> The web server is now available on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in the browser of your choice
