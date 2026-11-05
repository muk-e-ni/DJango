# Customizing Admin Form 

Django creates default admin forms automatically using different templates. To edit different parts of a form, a class with edits can be passed to the admin.site.register() to modify the defaults added as a second argument. 

```
from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "q_text"]


admin.site.register(Question, QuestionAdmin)
```
The code above makes pub_date come before the Question field. 

## Spliting Related Fields with Fieldsets 
```
from django.contrib import admin

from .models import Question


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["q_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]


admin.site.register(Question, QuestionAdmin)
```
The first element of each tuple in fieldsets is the title of the fieldset. 

## Adding Related Objects

The next thing now would be to allow the admin to choose various choices. There are two ways to achieve this. 

The first one is just registering the Choice class. Then, from the Choice view we can choose the question to modify answers for in the select box. 

```
from django.contrib import admin

from .models import Choice, Question

# ...
admin.site.register(Choice)

```

The second way and the most effective way is by making a class for the choice and including it as an inline item on the created QuestionAdmin class. 

```
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["q_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)

```
This simply tells Django that "Choice"objects are edited on the Question admin page. 

## Modifying Choices Display

Choices takes a lot of screen space to display all the fields in admin.StackedInline. Using TabularInline is much more compact and cleaner. 
```
class ChoiceInline(admin.TabularInline): ...
```

## Customozing the Admin Change List 
By default, Django displays the str() of each object. But sometimes it would be helpful to display individual fields. In this case the page that displays all the questions. 

```
class QuestionAdmin(admin.ModelAdmin):
    # ...
    list_display = ["question_text", "pub_date", "was_published_reccently"]
```
>>Note: Sorting by the output of an arbitrary method doesn't work. So the was_published_recently method doesn't support ordering or sorting. 

Each line of the header contains a string representation of the output. But can be altered using the display decorator on that method. Here's an example.

```
from django.contrib import admin


class Question(models.Model):
    # ...
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

```

In addition to the list_display, the list_filter can also be used to add a filter side bar. A search field can also be included using search_fields. 

## Customizing the Admin Look and Feel 

To override the templates, one way is by copying the template to be changed and including it in the templates folder inside the project folder. The templates folder must be referenced in settings.py under:
DIRS: [BASE_DIR / "templates"]

DIRS is a list of filesystem directories to check when Django loads templates. 

Inside the created templates directory, an admin directory should be added and all the templates to be modified are copied here from BASE_DIR/<Project_folder>/admin

>> tip: To find the base path: #python -c "import django; print(django.__path__)"

Some files that can be edited include index.html, base.html, base_site.html: 

base_site.html
```
{% block branding %}
<div id="site-name"><a href="{% url 'admin:index' %}">Polls Administration</a></div>
{% if user.is_anonymous %}
  {% include "admin/color_theme_toggle.html" %}
{% endif %}
{% endblock %}
```
