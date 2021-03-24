import requests
import pprint  # beautifies printing
from bs4 import BeautifulSoup  # for scraping

# check scraping parameters by adding /robots.txt to end of a website


hn = []  # empty list to fill with selected articles


def sort_articles(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)  # sort articles by # of votes using the votes key


# create a function that grabs the title, link, and score of each article on the homepage.
def create_custom_hn_feed(info, sbtxt):
    for i, item in enumerate(info):
        title = item.getText()  # removes the html fodder leaving only the text of interest
        href = item.get('href', None)  # obtains link, if none present return None
        score = sbtxt[i].select('.score')  # obtain the score from the subtexts
        if len(score):
            votes = int(score[0].getText().replace(' points', ''))  # removes the fodder from string and produces an int
            if votes > 99:  # only keep articles with 100 or more votes
                hn.append({'title': title, 'link': href, 'votes': votes})  # creates dict with titles, links, and votes
    return sort_articles(hn)


def scrape_hackernews():
    """
    scrape Hacker News pages 1-5 for articles >100 votes and subsequently ranks them
    """
    links_titles, subtext = [], []
    for num in range(1, 6):
        pnum = str(num)
        res = requests.get(
            'https://news.ycombinator.com/news?p=' + pnum)  # create a response variable to obtain a given page
        soup = BeautifulSoup(res.text, 'html.parser')  # parses data from a given language into a Python object
        links_titles += soup.select('.storylink')  # obtains links and titles of stories (list form)
        subtext += soup.select('.subtext')  # grab the subtext of the articles (which contain the # of votes)
    pprint.pprint(create_custom_hn_feed(links_titles, subtext))


if __name__ == '__main__':
    scrape_hackernews()
