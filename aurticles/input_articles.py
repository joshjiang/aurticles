from feed.models import Article
import datetime

with open("your_saved_items.html") as fp:
    soup = BeautifulSoup(fp, "lxml")

all_articles_dictionary = {}
pp = pprint.PrettyPrinter(indent=4)
article_id = 0

for link in soup.find_all("div", {"class" : "_2pin" }):
    article_id += 1
#     pp.pprint(str(link.div.div.div.div.div))
    single_article_dictionary = {}
    post_section = 0

    for string in link.div.div.div.div.div:
        post_section += 1
        if post_section is 1:
            single_article_dictionary["hyperlink"] = str(string)[5:len(string)-7]
        if post_section is 2:
            single_article_dictionary["title"] = str(string)[5:len(string)-7]
        if post_section is 3:
            single_article_dictionary["publisher"] = str(string)[5:len(string)-7]
    all_articles_dictionary[article_id] = single_article_dictionary

for article in all_articles_dictionary:
    Article.objects.create(publisher=article["publisher"], title=article["title"], hyperlink=article["hyperlink"], body= "", time_published=datetime.datetime.now, time_added=datetime.datetime.now)
