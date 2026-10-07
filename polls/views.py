from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question as Q 
from django.http import Http404


def index(request):
    return HttpResponse("Hello, world, I am creating a Polls App")

def dashboard(request):
    questions = Q.objects.all()

    context = {
        "questions":questions 
    }
    return render(request, "polls/dashboard.html", context)

def detail(request, q_ID):
    question = get_object_or_404(Q, pk=q_ID)
    return render(request, "polls/questiondetail.html", {"question": question})

    