# python-examples
Examples for use in tutoring a python class.

> Demonstrates code and topics from:
> * Flask
> * MySQL
> * SQLite
> * Extract SQL and export to:
>   * CSV
>   * JSON

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

> The web server is now available on [http://localhost:5000/](http://localhost:5000/) in the browser of your choice.

### Using MySQL

1. Create a database named `mydatabase` on your MySQL Server
2. Create a `settings.py` file in the `mymodules` directory with the following dictionary (replacing user and password):

```python
settings = {
    "user": "lybekk",
    "password": "11234_4321password__PWD_PASS_WORD_p455w0rd"
}
```

## Jupyter Notebook

### Jupyter Web Server
* Run `jupyter notebook` from a folder containing a Jupyter notebook.
* Visit http://localhost:8888/

### Visual Studio Code
* Select an environment, use the `Python: Select Interpreter command` from the Command Palette (Ctrl+Shift+P)
* Create a Jupyter Notebook by running the `Python: Create Blank New Jupyter Notebook` command from the Command Palette (Ctrl+Shift+P) or create a new .ipynb file in your workspace.

## Notes

This project does not implement all security best practices. 
Take necessary precautions according to your environment when deploying applications in production.

* HTTPS
* SQL Injection
* XSS 

https://flask.palletsprojects.com/en/1.1.x/security/