# hired-gun

A webapp for freelancers to track clients, projects, work sessions, and invoices

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
  - Determine what views you want
    - For the beginning, stick with one ListView and one DetailView per model
  - `urls.py`
  - HTML templates
  - `views.py`
- Tests
  - Now start writing tests for the existing code
  - From now on, go TDD and write tests first
- Static files
  - Start with a CSS and a logo or background image
- Users
  - Create a login functionality
