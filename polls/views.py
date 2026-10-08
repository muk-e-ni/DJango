from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question as Q 
from django.db.models import F
from .models import Choice
from django.http import Http404
from django.urls import reverse 
from django.views import generic


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    model = Q


class DashboardView(generic.ListView):
    context_object_name = "latest_questions"
    template_name = "polls/dashboard.html"

    
    def get_queryset(self):
        return Q.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    template_name = "polls/questiondetail.html"
    model = Q

def vote(request, q_ID):
    question = get_object_or_404(Q, pk=q_ID)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/questiondetail.html", {
                  "question": question, 
                 "error_message": " You didn't select a valid option. Please select a valid option and try again."
            })
    
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))    



class ResultsView(generic.DetailView):
    template_name = "polls/results.html"
    model = Q
    
    
    