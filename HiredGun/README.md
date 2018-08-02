# How to try out locally

- `git clone` this repository
- Run `python3 manage.py migrate`
- Load some example data into the database by running:
```
python3 manage.py loaddata projects/fixtures/Client.json 
python3 manage.py loaddata projects/fixtures/Project.json 
python3 manage.py loaddata projects/fixtures/Session.json 
```
- Browse to <http://127.0.0.1:8000/projects> and view/edit/delete some data of your own
