This project aims at building a simple microblog using Flask. It starts with very basic Flask setup and then goes forwards to build a microblog based on SQLAlchemy.

Installation
------------
 1. Setup a virtualenv (`pip install virtualenv`)
    ```
    virtualenv virtualenv_flask --no-site-packages
    ```
 2. Activate your virtualenv
    ```
    source virtualenv_flask/bin/activate
    ````
 3. Install all the requirements
    ```
    pip install -r requirements.txt
    ```
 
**Note:** To deactivate the virtualenv, type `deactivate`

Running
-------
If your folder has `manage.py`, type `./manage.py runserver`
Otherwise use `python app.py`