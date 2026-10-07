# Views Overview
A views is a web page in the Django appliation that serves a specific function and has a specific template.
eg.
**Blog Sections** : Contains or holds various blog blog categories.
**Comment Action** : Handles posting comments to a given blog entry.

The pollsApp will have the following views:
- ***Question index page*** : displays the latest few questions
- ***Question Detail page*** : displays a question text, with no results but with a voting form.
- ***Vote Results page*** : displays results for a particular section.
- ***Vote Action*** : displays results for a particular section. 

In Django, web pages and other content are delivered using views. URLconf files maps URL patterns to view functions. 

## Working with Views
Views are configured in the views.py of every app. Every view is defined in a function. Every view processes a request and sends an HTTP Response. 

After defining views, they must be added to the URLConf of the app itself. 

Each view can either return a Response or an HTTP404. 

The following is an example of a view code:
```
from django.http import HttpResponse

from .models import Question


def dashboard(request):
    questions = Q.objects.all()
    output = ''.join([q.q_text for q in questions])

    return HttpResponse(output)
```
For the above code, the design is hardcoded in the code. Django allows usange of templates that must be defined in every app.

![Django screenshot showing the qustions view hard-coded version](/images/regular_question_detail.png)

Every app must have a templates directory, then inside it another directory with the same name as the app then the templates go inside. For example,

`/polls/templates/polls/dashboard.html`

```

{% if questions %}
    <ul>
        {% for q in questions %}
            <li><a href="/polls/{{q.id}}/"> {{q.q_text}}</a></li>

        {% endfor %}
    </ul>
{% else %}
    <p> No questions Available</p>
{% endif %}
```

To use the template inside the view, instead of the hard coded code, the loader class is used from the module django.template.

```
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question as Q 
from django.template import loader


def index(request):
    return HttpResponse("Hello, world, I am creating a Polls App")

def dashboard(request):
    questions = Q.objects.all()

    template = loader.get_template("dashboard.html")
    context = {
        "questions":questions 
    }

    return HttpResponse(template.render(context, request))

```

So the above code does the following:
 1. loads the the template from templates/polls/dashboard.html
 2. Passes context. The context is a dictionary mapping tempalate variable names to python objects. 

 ![Django screenshot showing the template version](/images/question_detail_template.png)

Since this is a common practice, Django has the following render shortcut in the shortcuts module.
 ```
from django.shortcuts import render

from .models import Question


def dashboard(request):
    questions = Q.objects.all()

    context = {
        "questions":questions 
    }
    return render(request, "polls/dashboard.html", context)

    
 ```

loader and HTTPResponse are no longer needed here. The render function takes the request object as the first arguement, a template and a dictionary for the context. Then it returns an HTTPResponse object of the given template rendered with the given context. 


### Raising a 404 error 
The following code generates a 404 if the question being queried doesn't exist. 
```
from django.http import Http404
from django.shortcuts import render

from .models import Question


# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

```

The get_object_or_404() function simplifies this by taking a Django model as its first argument and an arbitrary number of keyword arguments, which it passes to the get() function. If the object doesn't exist, a 404 is thrown.
```
#/polls/views.py
def detail(request, q_ID):
    question = get_object_or_404(Q, pk=q_ID)
    return render(request, "polls/questiondetail.html", {"question": question})
```
```
#/polls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("<int:q_ID>/", views.detail, name="detail"),
]
```

>> The reason why using a helper function get_object_or_404() instead of automatically catching the ObjectDoesNotEXIST Exceptions at a higer level or having the model API raise HTTP404  is because that would couple the model layer to the view layer. And one of DJango's foremost design goal is to maintain loose coupling. 

There's also a get_list_or_404() func that works just like the object one but it uses filter() instead of get(). 

### Removing Hardcoded URLS

 In a project with many apps, URL names might be similar.A namespace is added to the URLconf in the polls/urls.py so that DJjango knows what url to match. 

 ```
from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
 ```