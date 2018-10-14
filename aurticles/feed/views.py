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
from datetime import datetime
from newspaper import Article as news_article
import re
import nltk
from gtts import gTTS



# from .forms import GameForm, PlayerForm
from .models import Article


def index(request):
    latest_article_list = Article.objects.order_by('-time_published')
    context = {'latest_article_list': latest_article_list}
    return render(request, 'feed/base-index.html', context)


def get_articles(request):
    Article.objects.all().delete()
    article_table = get_articles_table("feed/your_saved_items.html")
    for article in article_table:
        a = Article.objects.create(categories=article_table[article]["categories"],publisher=article_table[article]["publisher"], title=article_table[article]["title"], hyperlink=article_table[article]["hyperlink"], audio_filename=article_table[article]["audio_filename"], body=article_table[article]["body"],time_published=article_table[article]["time_published"], time_added=timezone.now())
        a.save()
    return render(request, 'feed/base-get-articles.html')

def detail(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    context = {"article":article}
    return render(request, 'feed/base-detail.html', context)



def get_articles_table(input_file):
    with open(input_file) as fp:
        soup = BeautifulSoup(fp, "lxml")

    all_articles_dictionary = {}
    article_id = 0
    
    
    for link in soup.find_all("div", { "class" : "uiBoxWhite" }):
        single_article_dictionary = {}
        post_section = 0
        link_content = link.find("div", { "class" : "_2pin" })
        if link_content == None:
            continue 
        for link_string in link_content.div.div.div.div.div:
            post_section += 1
            decoded_string = str(link_string).replace('\r\n', '\n')
            article_post = True

            if post_section is 1:
                if decoded_string[5:9] != "http":
                    post_section = 0
                    article_post = False
                    exit
                else:
                    single_article_dictionary["hyperlink"] = decoded_string[5:len(link_string)-7]
            if post_section is 2:
                single_article_dictionary["title"] = decoded_string[5:len(link_string)-7]
#                 if post_section is 3:
#                     single_article_dictionary["publisher"] = decoded_string[5:len(link_string)-7]
        # time published 
#         Oct 05, 2018 6:45pm
        
        single_article_dictionary["time_published"] = datetime.strptime(str(link.find("div", {"class":"_2lem"}).get_text()), "%b %d, %Y %I:%M%p")

        if "saved a link from" in str(link.find("div", {"class":"_2lel"}).get_text()):
            publisher_string = re.search('saved a (.*) post', str(link.find("div", {"class":"_2lel"}).get_text()))
            single_article_dictionary["publisher"] = publisher_string.group(1)[:len(publisher_string.group(1))-2].replace('link from','')
        else:
            single_article_dictionary["publisher"] = ""
            
        
        if article_post:
            article = news_article(single_article_dictionary["hyperlink"])
            article.download()
            try:
                article.parse()
                single_article_dictionary["body"] = article.text
                # tts = gTTS(single_article_dictionary["body"], lang='en')
                article.nlp()
                single_article_dictionary["categories"] = article.keywords
                # tts.save(single_article_dictionary["title"] + ".mp3")
                single_article_dictionary["audio_filename"] = single_article_dictionary["title"] + ".mp3"
                
            except:
                single_article_dictionary["body"] = "Article could not be found :("
                single_article_dictionary["audio_filename"] = "No audio :("
            article_id += 1               
            all_articles_dictionary[article_id] = single_article_dictionary
        if article_id >=10:
            break
    



    return all_articles_dictionary
