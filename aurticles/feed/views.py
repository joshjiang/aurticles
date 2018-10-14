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
    latest_article_list = Article.objects.order_by('-time_published')
    context = {'latest_article_list': latest_article_list}
    return render(request, 'feed/base-index.html', context)

def get_articles(request):
    article_table = get_articles_table("feed/your_saved_items.html")
    for article in article_table:
        a = Article.objects.create(publisher=article_table[article]["publisher"], title=article_table[article]["title"], hyperlink=article_table[article]["hyperlink"], body= "", time_published=timezone.now(), time_added=timezone.now())
        a.save()
    return render(request, 'feed/base-get-articles.html')

def get_articles_table(input_file):
    with open(input_file) as fp:
        soup = BeautifulSoup(fp, "lxml")

    all_articles_dictionary = {}
    article_id = 0

    for link in soup.find_all("div", { "class" : "_2pin" }):
        single_article_dictionary = {}
        post_section = 0

        for link_string in link.div.div.div.div.div:
            post_section += 1
            decoded_string = str(link_string).replace('\r\n', '\n')
            article_post = True

            if post_section is 1:
                # if this is not a URL or a link to a post then skip it
                # print(decoded_string[5:9])
                # print(decoded_string[5:9] != "http")
                if decoded_string[5:9] != "http":
                    post_section = 0
                    article_post = False
                    exit
                else:
                    single_article_dictionary["hyperlink"] = decoded_string[5:len(link_string)-7]
            if post_section is 2:
                single_article_dictionary["title"] = decoded_string[5:len(link_string)-7]
            if post_section is 3:
                single_article_dictionary["publisher"] = decoded_string[5:len(link_string)-7]
        if article_post:
            article_id += 1                            
            all_articles_dictionary[article_id] = single_article_dictionary

    return all_articles_dictionary