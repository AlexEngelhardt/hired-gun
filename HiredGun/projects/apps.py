from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    # This is currently not in use. If I set INSTALLED_APPS to 'projects.apps.ProjectConfig' instead of 'projects', then my static files aren't found anymore.
    name = 'projects'
