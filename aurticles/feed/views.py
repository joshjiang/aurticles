from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.http import JsonResponse

from django.views.generic import FormView

# from .forms import GameForm, PlayerForm
# from .models import Game, Player


def index(request):
    # latest_article_list = Game.objects.order_by('-pub_date')[:5]
    # context = {'latest_article_list': latest_article_list}
    return render(request, 'feed/index.html')
