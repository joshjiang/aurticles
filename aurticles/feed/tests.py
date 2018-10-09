from django.test import TestCase
from bs4 import BeautifulSoup
import requests


class ArticleModelTests(TestCase):

    def test_beautiful_soup_article_creation(self):
        """
        beautiful soup parses through the user's HTML file and gets each 
        link's article's body text
        """
        r = requests.get("static/your_saved_items.html")

        data = r.text

        soup = BeautifulSoup(data, "lxml")
        html = ""
        i = 0

        # parse through individual pieces of the courseblocktitle string, such as course num
        for link in soup.find_all("div", {"class": "courseblock"}):

            courseBlock = link.find("p", {"class": "courseblocktitle"})
            courseBlock = courseBlock.get_text()
            courseTuple = [x.strip() for x in courseBlock.split('.')]
            courseTuple[0] = courseTuple[0].replace(u'\xa0', u' ')
            # print(courseTuple)

            courseDesc = link.find("p", {"class": "courseblockdesc"})
            courseDesc = courseDesc.get_text()

            # format html table
            html += """    
            <tr data-toggle="collapse" data-target="#course_""" + str(i) + """" class="accordion-toggle music-course">
            <th scope="row">""" + courseTuple[0] + """</th>
            <td>""" + courseTuple[1] + """</td>
            <td>""" + courseTuple[2] + """</td>
            </tr>
            <tr>
                <td colspan="6" class="hiddenRow">
                    <div class="accordion-body collapse" id="course_""" + str(i) + """">""" + courseDesc + """</div>
                </td>
            </tr>
            """

            i += 1

            with open("index.html", "w") as file:
            file.write(html)        self.assertIs(future_question.was_published_recently(), False)





