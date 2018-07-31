# hired-gun

A webapp for freelancers to track clients, projects, work sessions, and invoices

### Django notes

Best order for creating a new app:

- Create Models
  - Determine your models, fields, and relationships
  - Create the `models.py`
- `admin.py`: Create admin views
- Fixtures
  - From the admin backend, add sample data and export it to JSON fixtures
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
