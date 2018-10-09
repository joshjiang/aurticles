from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from django.utils import timezone
from django.http import JsonResponse
from bs4 import BeautifulSoup
from django.views.generic import FormView
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils import timezone


# from .forms import GameForm, PlayerForm
from .models import Article


def index(request):
    article_table = get_articles_table("feed/your_saved_items.html")
    for article in article_table:
        a = Article.objects.create(publisher=article_table[article]["publisher"], title=article_table[article]["title"], hyperlink=article_table[article]["hyperlink"], body= "", time_published=timezone.now(), time_added=timezone.now())
        a.save()
    latest_article_list = Article.objects.order_by('-pub_date')[:5]
    context = {'latest_article_list': latest_article_list}
    return render(request, 'feed/base-index.html')

def get_articles_table(input_file):
    with open(input_file) as fp:
        soup = BeautifulSoup(fp, "lxml")
    all_articles_dictionary = {}
    article_id = 0

    for link in soup.find_all("div", { "class" : "_2pin" }):
        article_id+=1
    #     pp.pprint(str(link.div.div.div.div.div))
        single_article_dictionary = {}
        post_section = 0

        for string in link.div.div.div.div.div:
            print(str(string))
            post_section+=1
            if post_section is 1:
                single_article_dictionary["hyperlink"] = str(string)[5:len(string)-7]
            if post_section is 2:
                single_article_dictionary["title"] = str(string)[5:len(string)-7]
            if post_section is 3 :
                single_article_dictionary["publisher"] = str(string)[5:len(string)-7]
        all_articles_dictionary[article_id] = single_article_dictionary

    return all_articles_dictionary