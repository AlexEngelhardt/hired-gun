# hired-gun

A webapp for freelancers to track clients, projects, work sessions, and invoices

### How to try this out locally

- `git clone` this repository
- Run `python3 manage.py migrate`
- Load some example data into the database by running:
```
python3 manage.py loaddata projects/fixtures/auth.json
python3 manage.py loaddata projects/fixtures/Client.json 
python3 manage.py loaddata projects/fixtures/Project.json 
python3 manage.py loaddata projects/fixtures/Session.json 
```

- Run `python3 manage.py runserver` to start your local development webserver
- Browse to <http://127.0.0.1:8000>
- Login as user `test` with password `test`
  - The user `admin` with password `adminadmin` exists too.
- Go view/edit/delete some data, and build a few reports!

### How to deploy on AWS / Elastic Beanstalk

See [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)

### Django notes

Best order for creating a new app:

- Determine apps and models
  - Try to predict the final models and relations as best as possible
  - Find out how to best split it in apps for now
  - Start with only one app here, though
- Create Models
  - Determine your models, fields, and relationships
  - Create the `models.py`
- `admin.py`: Create admin views
  - To login to the admin backend and verify:
    - Update `settings.py`: add ProjectsConfig to `INSTALLED_APPS`
    - `makemigrations projects` 
    - `migrate`
- Fixtures
  - From the admin backend, add sample data
  - export all models to JSON fixtures: `python3 manage.py dumpdata --indent=4 projects.Client > projects/fixtures/Client.json` (etc. for Project and Session)
- Frontend:
  - For the beginning, stick with one ListView and one DetailView per model
  - `urls.py`
  - `views.py`
  - HTML templates
  - Try these views.
  - If they work, determine what other views you want
	- that's probably "create, update, delete", for now
- Tests
  - Now start writing tests for the existing code
  - From now on, go TDD and write tests first
- Static files
  - Start with a CSS and a logo or background image
- Users
  - Create a login functionality
