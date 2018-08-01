from django.contrib import admin

from .models import Project, Client, Session


#### Clients

class ProjectInline(admin.TabularInline):  # or admin.StackedInline if you prefer the ugly version :)
    """
    Conveniently enter foreign key relationships. 
    Allows to create a set of projects within the add-client
    admin form. See here:
    https://docs.djangoproject.com/en/2.0/intro/tutorial07/
    """
    model = Project
    extra = 1  # by default, add enough fields for 'extra' projects

class ClientAdmin(admin.ModelAdmin):
    """
    Here I'm creating subsections for the "many" fields, and also
    changing the order of how the fields appear in the admin form
    """
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Payment information', {'fields': ['payment_terms', 'invoice_email', 'billing_address']})
    ]
    inlines = [ProjectInline]

admin.site.register(Client, ClientAdmin)


#### Projects

class ProjectAdmin(admin.ModelAdmin):
    """
    By default, the list view in an admin panel only shows the __str__ of a project.
    Here, we specify fields to show in a more detailed, tabular view.
    Note: We can also use *methods* of a model, not only fields!
    """
    # Don't use all fields, you'll bloat the view:
    list_display = ('name', 'client', 'start_date', 'is_active')
    list_filter = ['start_date', 'end_date']
    search_fields = ['name']

admin.site.register(Project, ProjectAdmin)


#### Sessions

admin.site.register(Session)
