from html.parser import HTMLParser
import argparse
import requests

parser = argparse.ArgumentParser(
    "linkchecker", description="Recursively check a URL exists, and check the links on that page, etc.")
parser.add_argument("url", help="The Starting URL to check", type=str)
parser.add_argument(
    "--delay", help="Time in ms between requests, default=10", default=10)
args = parser.parse_args()

urls = []


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if (tag == 'a'):
            add_url(attrs["href"])


parser = MyHTMLParser()


def add_url(url):
    try:
        existing = next(x for x in urls if x.url == url)
    except StopIteration:
        existing = None

    if (existing):
        return

    # @todo don't allow other domains, or rather check them
    # but don't parse them for other links

    urls.append({
        "url": url,
        "parsed": False,
        "code": None,
    })


def next_url():
    return next(url for url in urls if url["parsed"] == False)


def parse_url(url):
    r = requests.get(url)
    parser.feed(r.text)


def run():
    url = next_url()

    while url:
        print("Checking", url)
        url = next_url()


add_url(args.url)
run()
