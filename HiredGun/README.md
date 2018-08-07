
### TODOs

/* also see Arc project sheet */

/* also grep this repo for TODO within .py files */

**Reports forms.Forms**

- Empty 'client' fields still fail. A custom widget may help, which would make the empty choice 'disabled' instead of passing ""
- The ModelMultipleChoiceField gets passed in the GET url as `&project=1&project=2`. My code currently takes the last project only there; it doesn't check if there's multiple projects submitted.

**Authentication**

- read official docs
- cross-check with DjangoGirls tutorial


**Add/Edit session form**

- Selecting the project should be hierarchical, by first selecting the client, then the project.
  - Ideally:
	- Select the client not from a dropdown, but from a one-click list
      - Then a conditional display of projects
- Behind "units worked", you should print the actual unit (day, hour, or fixed)
- When editing, the 'date' field is not populated with the existing date. Maybe because the format in the HTML form is `mm/dd/yyyy` when it should be `yyyy-mm-dd`?


**General**

- Unify language or add i18n
  - Why do I have a comma as decimal sign, not a period?
- All "delete" buttons should have a confirmation pop-up, or redirect to a dedicated confirmation template.
- The Session model should have functions `units_worked()` and `money_earned()` so that I can compute reports
  - Ideally: Never compute this redundantly. Currently, you are. (see `reports/views.py:get_total_earned()`)
- The date in the ModelForms (i.e. on the frontend) should be shown as yyyy-mm-dd


**Someday/Maybe**

- Use [django-tables2](https://django-tables2.readthedocs.io/en/latest/) instead of manually written HTML tables. They are also sortable by column

**Testing**

- Start with tests asap. Wait too long and it won't happen :)
