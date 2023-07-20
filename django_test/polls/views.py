from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]

#     # version sans template
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)

#     # version avec template
#     # fait référence aux variables appelées dans le template
#     context = {
#         "latest_question_list": latest_question_list,
#     }
#     # template = loader.get_template("polls/index.html")

#     # return HttpResponse(template.render(context, request))

#     # version avec template raccourcie
#     # render prend request, path_template, dict (opt)
#     return render(request, "polls/index.html", context)


# def detail(request, question_id):
#     # version sans template
#     # return HttpResponse("You're looking at question %s." % question_id)


#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")

#     # version raccourcie
#     question = get_object_or_404(Question, pk=question_id)

#     return render(request, "polls/detail.html", {"question": question})


# def results(request, question_id):
#     # response = "You're looking at the result of question %s."
#     # return HttpResponse(response % question_id)

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

# def vote(request, question_id):
#     # return HttpResponse("You're voting on question %s." % question_id)

#     question = get_object_or_404(Question, pk=question_id)

#     try:
#         selected_choice = question.choice_set.get(pk=request.POST["choice"])
#         # request.POST sont toujours des str
#     except (KeyError, Choice.DoesNotExist):
#         # redisplay question voting form
#         return render(
#             request,
#             "polls/detail.html",
#             {
#                 "question": question,
#                 "error_message": "You didn't select a choice.",
#             },
#         )
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()

#         # toujours redirect après un POST successful pour éviter double post
#         return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# nouvelle implémentation avec des templates generiques de django
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions (not including those set
        to be published in the future)."""

        # bugged return
        # return Question.objects.order_by("-pub_date")[:5]

        # fixed return
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


# repris
def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)

    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # request.POST sont toujours des str
    except (KeyError, Choice.DoesNotExist):
        # redisplay question voting form
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # toujours redirect après un POST successful pour éviter double post
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )
