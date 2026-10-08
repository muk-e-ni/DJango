# Forms and Generic Views

This part covers voting functionanlity and simplifying the view creation process. 

## Voting Form 
To give the voting view functionality, the following updated template is used. It contains the form for filling out votes.

```
<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
<fieldset>
    <legend><h1>{{ question.question_text }}</h1></legend>
    {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    {% for choice in question.choice_set.all %}
        <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
        <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    {% endfor %}
</fieldset>
<input type="submit" value="Vote">
</form>
```

The template has:
- radio buttons associated with every choice's ID. The name of every radio button is "choice". This comes into play when one submits their vote. It acts as a key to the choice's ID. 

- forloop.counter - indicates how many times the for tag has gone through its loop. 
- {%csrt_token%} - this is beneficial when working with POST method in Django. It protects against CSRF (Cross Site Request Forgeries) and since POST modifies data, it's very helpful to use it in all forms that are targeted at internal URLs.

on the urls.py, there's this voting endpoint:
`path("<int:question_id>/vote/", views.vote, name = "vote")`

Now all that's needed is a view function.

```
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

```
On the above function there is:
1. **request.POST**: A dictionary-like objet that accesses submitted data by key name. Like stated before when a user submits their vote the "name = choice", choice will be used as the key name to the vote's ID. So here, the function is requesting for that ID.
2. **KeyError**: The request.POST['choice'] will raise a KeyError if there was vote submitted.
3. **F("Votes") + 1**: The F() function allows usage of model objects eliminating the need of having to export every field Object or the model as a whole. In this case, it is used to increase the votes field by one.
4. **HttpResponseRedirect**: This one takes a single argument: The URL to which the user will be redirected after voting. It is always essenstial when dealing with POST as it prevents data from being posted twice if a user hits the back button. 
5. **reverse()**: Avoids having to hardcode a URL in the view function. It takes the redirect view and the variable portion of the URL pattern that points to that view as args. 
Below is the result view function and the template.

```
#/polls/views.php
from django.shortcuts import get_object_or_404, render


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

```

```
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```
![Voting form](/images/voting_form.png)
![Vote results ](/images/vote_results_page.png)
## Generic Views 
Generic views eliminate having redundunt views. For instance, the votes view is similar to the dashboard view. They are simillar in that they have a common basib web development pattern: Getting data from the db according to a given parameter in the URL, loading a template and returng the rendered template.

### Modifying Everthing to Use Generic Views
steps:
1. Start with the URLconf
2. Delete uneeded views 
3. Introduce new Generic views

```
#/polls/urls.py

from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```
What's changed?
1. `<question_id> to <pk>`: Essential because the DeatilView() generic view will replace the detail() and result() views, and it expects the primary key value from the URL to be called pk.


Next up, ammending the views. 
```
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    # same as above, no changes needed.
    ...
````

Each generic view needs to know what model it will be acting upon. There are two ways of doing this:
1. Specifying the model eg. (model = Question)
2. Defining the get_queryset() method 

The default template is called <app name>/<mode name>_detail.html
To override the default template, a template_name is provided. eg. template_name="polls/results.html"

