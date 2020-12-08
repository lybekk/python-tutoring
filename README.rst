Python tutoring
===============

Examples for use in tutoring a python class.

    Demonstrates code and topics from:

    * Flask
    * MySQL (or MariaDB)
    * SQLite
    * Extract SQL and export to:
        * CSV
        * JSON

===========
First steps
===========

Install required Python packages
1. In your terminal, change path (:code:`cd`) to this project's directory
2. Run :code:`pip install -r requirements.txt`

*If `pip` doesn't work, try `pip3`*

    Some red warnings may appear. Ignore these, unless you experience errors when running scripts.

Flask Web Server
----------------

1. :code:`cd` to this project's directory
2. Run :code:`python server.py`
    * *Some platforms may use `python3` instead*

    The web server is now available on [http://localhost:5000/](http://localhost:5000/) in the browser of your choice.

Jupyter Notebook
----------------

Jupyter Web Server
^^^^^^^^^^^^^^^^^^

* Run :code:`jupyter notebook` from a folder containing a Jupyter notebook.
* Visit http://localhost:8888/

Visual Studio Code
^^^^^^^^^^^^^^^^^^

* Select an environment, use the "``Python: Select Interpreter``" command from the Command Palette (Ctrl+Shift+P)
* Create a Jupyter Notebook by running the "``Python: Create Blank New Jupyter Notebook``" command from the Command Palette (Ctrl+Shift+P) or create a new .ipynb file in your workspace.

Notes
-----

This project does not implement all security best practices. 
Take necessary precautions according to your environment when deploying applications in production.

* HTTPS
* SQL Injection
* XSS

[Flask Docs - Security](https://flask.palletsprojects.com/en/1.1.x/security/)

Documentation
-------------

Sphinx is used for generating documentation.

To build docs:
```shell
cd docs
make html
```
