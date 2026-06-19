from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Zwraca 5 najnowszych opublikowanych pytań (nie uwzględniając tych,
        których data publikacji jest w przyszłości).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Wyklucza pytania, które nie zostały jeszcze opublikowane.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Ponowne wyświetlenie formularza głosowania z błędem.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Nie wybrałeś żadnej odpowiedzi.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Zawsze zwracamy HttpResponseRedirect po udanym odebraniu danych POST.
        # Zapobiega to podwójnemu wysłaniu danych, jeśli użytkownik odświeży stronę.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))