
# Django Basics

## First things First: Installation

1. Setting up a virtual env: `python -m venv venv`
2. Installing Django: `pip install django`
3. verifying installation:
```
import django
print (django.get_version())
6.1.1
```
4. Creating a django project which is a collection of settings for an instance of django: `django-admin startproject <project_name> <folder_to_be_stored> `

## Exploring the Project Files
1. manage.py: a command-line utility that allows interaction with the project
2. PollAppSite: the actual python package.
* /__init__.py: An empty file that tells Python that this directory should be considered a Python package
* /settings.py: Settings/configuration for this Django project.
* /urls.py: The URL declarations for this Django project; a “table of contents” of the Django-powered site.
* /asgi.py: An entry-point for ASGI-compatible web servers to serve the project.
* /wsgi.py: An entry-point for WSGI-compatible web servers to serve the project

To verify everything works, run the manage.py script. 

![alt text](/images/initial_index.png)

>> App vs. Project
>>An app is a web application that does something. eg. a blog, a database that stores public records. A project is a collection of configurations and apps for a particular website. It can contain multiple apps. Apps in django can exist anywhere in the python path (in this case the PollAPP folder).

### Creating an APP
To create an app, Run the command `python manage.py startapp polls` in the same directory as manage.py. The newly created file structure will house the app.

### Creating Views 
to create  views, you have to edit the views.py in the app. So a view is basically a resource that the user can view from the browser. 

```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.") 
```

For it to be accessible, it must have a link defined in the URLConfiguration or URLConf for short.  These URL configurations are defined inside each Django app, and they are Python files named urls.py.

To define a URLconf for the polls app, create a file polls/urls.py with the following content:

``` 
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
] 
```

The last step now involves including the link in the main urls.py inside the project rather than the app. 

To do this, add an import for django.urls.include in PollsApp/urls.py and insert an include() in the urlpatterns list, so you have:

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("polls", include("polls.urls")),
    path("admin", admin.site.urls),
]
```

Path - takes at leat 2 arguments: route and view
Include - chops whatever part of url mathched up to that point and sends the remaining string to the included URLconf for further processing.

>> You should always use include() when you include other URL patterns. The only exception is admin.site.urls, which is a pre-built URLconf provided by Django for the default admin site.

To verify that everything worked, run the server again if reloader is off. Navigate to http://127.0.0.1:8000/polls/ 
if an error pops up here, confirm the url has /polls at the end and not just the port.



![Django screenshot showing the polls initial view](/images/polls_view.png)

