"""
Definition of urls for PeoplehrWeb.
"""

from datetime import datetime
from django.conf.urls import url
from django.conf.urls import include
import django.contrib.auth.views
from django.contrib import admin
from django.contrib import admindocs
import app.forms
import app.views
from app.views import home,about,contact


urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about')
]
