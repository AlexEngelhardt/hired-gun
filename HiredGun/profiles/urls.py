from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('profile/edit', views.update_profile, name='edit-profile'),
]
