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

### How to deploy on AWS

- [This official AWS doc](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html) didn't work for me out-of-the-box
- I wanted to "do it myself" as much as possible, for the learning effect and the higher amount of control.


- Start an Ubuntu (18.04) Server with public access.
- Run:
```
sudo apt-get update
sudo apt install apache2 apache2-dev virtualenv python3-dev python3-pip
sudo service apache2 restart
ln -sf /usr/bin/python3 /usr/bin/python

```
- Apache2 auto-starts on install. You should be able to browse to your instance's public IP now. If not, try `sudo service apache2 status`. Also check your instance's security group if the machine really is accessible from outside.
- Run:
```
sudo mkdir -p /var/www/apps/
cd /var/www/apps
git clone https://github.com/AlexEngelhardt/hired-gun.git
cd hired-gun
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
# Install wsgi from pip, not via 'apt install libapache2-mod-wsgi':
# https://stackoverflow.com/questions/41005030

# TODO maybe do this from *outside* the virtualenvironment ?
pip install mod_wsgi
```
- Add this to the bottom of `/etc/apache2/apache2.conf` (replacing the IP with your actual public IP):
```
WSGIScriptAlias / /var/www/apps/hired-gun/HiredGun/HiredGun/wsgi.py
WSGIPythonHome /var/www/apps/hired-gun/HiredGun/venv
WSGIPythonPath /var/www/apps/hired-gun/HiredGun

WSGIDaemonProcess 18.196.87.1 python-home=/var/www/apps/hired-gun/HiredGun/venv$
WSGIProcessGroup 18.196.87.1

<Directory /var/www/apps/hired-gun/HiredGun/HiredGun>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```
- Become root, activate your virtualenvironment, then run:
```
mod_wsgi-express start-server HiredGun/wsgi.py --port 80 --user www-data --group www-data
```

- Browse to your public IP at port :8000 and verify it's starting to look like your app (the static files don't work yet)


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
