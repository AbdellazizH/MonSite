from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.utils import timezone

from sondage.models import Question, Choice

# Create your views here.
# @login_required
def index(request):
    latest_question_list =Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    # latest_question_list =Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {'latest_question_list': latest_question_list}
    return HttpResponse(template.render(context, request))

# @login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            'detail.html',
            {
                'question': question,
                'error_message': "Vous n'avez pas sélectionné une réponse, veuillez en choisir une svp..."
            }
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('sondage:results', args=(question.id,)))

# @login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})
