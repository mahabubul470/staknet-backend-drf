[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Python](https://img.shields.io/pypi/pyversions/shurjopay-plugin)](https://badge.fury.io/py/shurjopay-plugin)
[![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.com/project/pip/)
> :notebook: **Note:** This django app is built with python version 3.12-dev
#### Step 1: Install Python and Activate Virtual Environment

For managing different versions of Python, we have used [pyenv](https://github.com/pyenv/pyenv-installer), a version management tool for python and used [pyenv/virtualenv](https://github.com/pyenv/pyenv-virtualenv) plugin for managing multiple virtual environments. This [intro to pyenv](https://realpython.com/intro-to-pyenv/) guide will help to install pyenv and how to work with it.

Here is a example of creating and activating a virtualenv using pyenv:

```
pyenv virtualenv 3.12-dev staknetenv
pyenv activate staknetenv
pyenv deactivate # to deactivate the virtualenv
```

#### Step 2: Install Project Requirements

```bash
pip install -r requirements.txt
```
#### Step 3: Create the .env file and configure it

```bash
cat _env_sample > .env
```


#### Step 4: Install MongoDB and MongoExpress

Yout can install Mongo & MongoExpress locally in your machaine or use docker 

```
docker compose up -d --build
```
#### You can run the project localy using

```bash
python manage.py runserver
```

> :notebook: **Note:** You dont need to migrate anything as using nosql for the primary database and mongoengine ODM insted of dajango ORM and PyMongo 

> :notebook: **Note:** No django admin, No Authenticaton backend from django/drf, Custom Token Authentication (JTW) Implemented.