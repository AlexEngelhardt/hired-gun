# TODOs

### Crucial for MVP release

- also grep this repo for TODO within .py files and migrate them here

**ASAP**

- Better reports:
  - YTD earned. With graphs.
  - Separate Cashflow from earned. I.e., sessions from invoice_paids
- Add client form:
  - Hide the 'user' field, pre-set it with the logged in user
- Add project form:
  - Doesn't subset clients to those of the logged in user anymore
- Get all sessions that are not yet invoiced 

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
  - Use 'django-wkhtmltopdf' instead of reportlab, you can create and transform an invoice HTML easily instead of having to draw the whole PDF by hand
  - i.e., start with a HTML invoice
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
- Make a css with e.g. div class="A4invoice". It should span 21*29cm and have classes for the address, the footer, etc. 
- Don't store the client ID in an invoice. Instead, put get_client() method in the invoice model
  - => you have to build a custom model validator for an invoice: all its assigned projects must belong to the same client
- In "add invoice", the form's client field is not really readonly, I can change it. The "disabled" attribute doesn't submit the client - what do? Keep it empty and add the client in Python instead?

**Prettier**

- Put Forms in tables at least :)
- Input field width narrower (4 digits year, e.g.)
- Dropdown menus (you need JavaScript for that)

### Someday/Maybe

- Use [django-tables2](https://django-tables2.readthedocs.io/en/latest/) instead of manually written HTML tables. They are also sortable by column
- Multiple currencies besides €

**Invoices**

- I should make sure that a Session can only be billed in *one* Invoice. How? An extra table 'session_invoice' where constraint PK=(session, invoice)?
  - Or: Validate on storing an invoice that the timespan and project list don't overlap with some other invoice

**Reports**

- Can reports.html use a generic list view? What's the advantage in such a (more custom) view?


**Forms**

- Choose ModelForm (`forms.py`) or manual ones (in `views.py`) for reports. Not both.
  - And by that I mean: switch to ModelForms
- Instead of having multiple forms, you can play with JavaScript (I think AJAX or jQuery are the magic words here), to only show the "project" field after one or more "clients" have been selected. Then you can have just one form that shapeshifts based on what you entered
- The Password reset email doesn't work because Django can't send emails yet.
- Use django-datetimepicker for all forms' date fields 

**Misc/Fun**

- Build some REST(ful?) API in the app, just to find out what exactly that is.
- Lint your project: `python3 -m flake8` from the project root
- Build a FormMixin and consolidate e.g. ClientCreateView and ClientUpdateView
  - See `ProductFormMixin` in GSA/product/views.py
- Payment terms: 2% 10 Net 30, COD, and PIA don't yet work in the invoice app: You need to set a due date
