# TODOs

### Crucial for MVP release

- also grep this repo for TODO within .py files and migrate them here

**Authentication**

- Signup as a demo user: without e-mail required, and sample-data auto-installed.
- **If you're not logged in, pull fixture session/project/users and use your request.session stuff to store the current setup. This is your demo user**
  - => Read up on Django's session framework
- **Or, just allow people to sign up without email**
- Find out how to build a demo user who can:
  - be logged in by multiple people more than once
  - gets its own clients, sessions, etc. to play around, but after the session is done, this gets destroyed
	- This is not to restrict usage, but to allow curious people to play around without registering a "proper" account
    - Alternatively (or, additionally): Allow creation of users where data gets destroyed after 14 days
  - Or just leave it all open for the beginning


**Testing**

- Start with tests asap. Wait too long and it won't happen :)
- Then move to test-driven development
- Try [PXP](http://alpha-epsilon.de/programming/2017/12/06/personal-extreme-programming/), maybe


**Reports**

- Output reports as PDF
  - Either with a Latex engine, or markdown/pandoc, or that python module `reportlab`
  - Emergency solution: An HTML popup that's then printable
- Cashflow (i.e. money in bank, instead of money worked): Use the invoices' `paid_date` attribute instead of session dates
- Yearly overview
  - A table with columns year, month, $ worked, cashflow in, YTD $ worked
  - Maybe include a matplotlib/seaborn plot on that page?
- List unpaid invoices
- List overdue invoices
  

**Add/Edit session form**

- Selecting the project should be hierarchical, by first selecting the client, then the project.
  - Ideally:
	- Select the client not from a dropdown, but from a one-click list
      - Then a conditional display of projects
- Behind "units worked", you should print the actual unit (day, hour, or fixed).
  - Problem: This depends on the client. 
  - Maybe refactor UI so that you have to add a session from a project detail view (or as a button in the project list view)?
  - Or that AJAX/jQuery thing


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
  - Either add attribute 'invoiced' to a session, or with an m:n table of invoices:sessions
- How to ensure invoice no. uniqueness and continuity?
- Build the `compute_due_date()` method
- Build the `generate_invoice_number()` method


**Prettier**

- Put Forms in tables at least :)
- Input field width narrower (4 digits year, e.g.)
- Dropdown menus (you need JavaScript for that)

### Someday/Maybe

- Use [django-tables2](https://django-tables2.readthedocs.io/en/latest/) instead of manually written HTML tables. They are also sortable by column
- Multiple currencies besides €


**Reports**

- Can reports.html use a generic list view? What's the advantage in such a (more custom) view?


**Forms**

- Choose ModelForm (`forms.py`) or manual ones (in `views.py`) for reports. Not both.
- Instead of having multiple forms, you can play with JavaScript (I think AJAX or jQuery are the magic words here), to only show the "project" field after one or more "clients" have been selected. Then you can have just one form that shapeshifts based on what you entered
- The Password reset email doesn't work because Django can't send emails yet.
- Use django-datetimepicker for all forms' date fields 

**Misc/Fun**

- Build some REST(ful?) API in the app, just to find out what exactly that is.
- Lint your project: `python3 -m flake8` from the project root
