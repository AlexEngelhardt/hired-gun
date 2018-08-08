# TODOs

### Crucial for MVP release

- also grep this repo for TODO within .py files and migrate them here

**ASAP**

- Understand Python inheritance and class methods etc. for the next step:
- 3 Forms/Reports:
  - Simple (all sessions within month/date range)
  - per client (only one client)
  - per project(s) (>= 1 project)
  - Put the 3 forms in 3 URLs, in 3 different places (reports, then reports/client1/ , then reports/rpoject=1?roject=2?project=8)

**Testing**

- Start with tests asap. Wait too long and it won't happen :)
- Then move to test-driven development
- Try [PXP](http://alpha-epsilon.de/programming/2017/12/06/personal-extreme-programming/), maybe

**Reports**

- Output reports as PDF
  - Either with a Latex engine, or markdown/pandoc, or that python module `reportlab`
  - Emergency solution: A HTML popup that's then printable


**Reports forms.Forms**

- Empty 'client' fields still fail. A custom widget may help, which would make the empty choice 'disabled' instead of passing ""
- The ModelMultipleChoiceField gets passed in the GET url as `&project=1&project=2`. My code currently takes the last project only there; it doesn't check if there's multiple projects submitted.

**Authentication**

- read official docs
- cross-check with DjangoGirls tutorial
- Find out how to build a demo user who can:
  - be logged in by multiple people more than once
  - gets its own clients, sessions, etc. to play around, but after the session is done, this gets destroyed
	- This is not to restrict usage, but to allow curious people to play around without registering a "proper" account
    - Alternatively (or, additionally): Allow creation of users where data gets destroyed after 14 days
  - Or just leave it all open for the beginning
- Once auth works, you can have a demo user with fixtures, and an Alex user with your actual data => no more 2 sqlite DBs
  
**Add/Edit session form**

- Selecting the project should be hierarchical, by first selecting the client, then the project.
  - Ideally:
	- Select the client not from a dropdown, but from a one-click list
      - Then a conditional display of projects
- Behind "units worked", you should print the actual unit (day, hour, or fixed).
  - Problem: This depends on the client. 
  - Maybe refactor UI so that you have to add a session from a project detail view (or as a button in the project list view)?
  - Or that AJAX/jQuery thing
- When editing, the 'date' field is not populated with the existing date. Maybe because the format in the HTML form is `mm/dd/yyyy` when it should be `yyyy-mm-dd`?


**General**

- Unify language or add i18n
  - Why do I have a comma as decimal sign, not a period?
- All "delete" buttons should have a confirmation pop-up, or redirect to a dedicated confirmation template.
- The Session model should have functions `units_worked()` and `money_earned()` so that I can compute reports
  - Ideally: Never compute this redundantly. Currently, you are. (see `reports/views.py:get_total_earned()`)
- The date in the ModelForms (i.e. on the frontend) should be shown as yyyy-mm-dd
- What happens if you try to delete a client, but it still has projects and/or sessions attached? (on_delete=PROTECT oder so)

**Invoices App**

- How to *fix* sessions for a specific invoice? They should be non-mutable afterwards (or maybe only with a warning!)
- How to ensure invoice no. uniqueness and continuity?

### Someday/Maybe

- Use [django-tables2](https://django-tables2.readthedocs.io/en/latest/) instead of manually written HTML tables. They are also sortable by column
- Multiple currencies besides €


**Reports**

- Can reports.html use a generic list view? What's the advantage in such a (more custom) view?

**Forms**

- Choose ModelForm (`forms.py`) or manual ones (in `views.py`) for reports. Not both.
- Instead of having multiple forms, you can play with JavaScript (I think AJAX or jQuery are the magic words here), to only show the "project" field after one or more "clients" have been selected. Then you can have just one form that shapeshifts based on what you entered

**Misc/Fun**

- Build some REST(ful?) API in the app, just to find out what exactly that is.

