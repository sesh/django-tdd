# Getting Ready to Start Coding

This workshop uses Python 3 which you should install based on the instructions for your system.
We will create a Django project inside of a virtual environment.

To get started create a virtual environment with Python and activate it:

```bash
> python -m venv time_api_venv
```

The virtual environment should have activated automatically.
To activate it again in the future you need to `source` the activate script.

```bash
> source time_api_venv/bin/activate
```

Now, install the latest version of Django with `pip`.

```bash
(time_api_venv)> pip install -U django
```

Once you have Django installed it's time to start our project. We'll be building a simple API for checking the current time. Let's call the project "time_api".

```bash
(time_api_venv)> django-admin startproject time_api
```

It's good practice at this point to add a `.gitignore` file.
Let's make sure that we don't commit our virtual environment, our database or any compiled Python files.

Add this to a file called `.gitignore` in the root of your Django project:

```
time_api_venv
db.sqlite3
*.pyc
__pycache__
```

Initialise your git repository, and add our project files. It's handy to commit regularly so that you can step back through your work.

```bash
(time_api_venv)> git init
(time_api_venv)> git add .
(time_api_venv)> git commit -m "⚡️ Initial commit to our Time API"
```

Great.
You can now move on the to the next step where we will walk through the creation of our Time API.
