from html.parser import HTMLParser
from urllib.parse import urlparse
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
            for name, value in attrs:
                if name == 'href':
                    add_url(value)


parser = MyHTMLParser()


def add_url(url):
    if (url[0:1] == "/"):
        url = base_url + url

    try:
        existing = next(x for x in urls if x["url"] == url)
    except StopIteration:
        existing = None

    if (existing):
        return

    urls.append({
        "url": url,
        "parsed": False,
        "code": None,
        "error": None,
    })


def next_url():
    try:
        return next(url for url in urls if url["parsed"] == False)
    except StopIteration:
        return None


def handle_url(url):
    print("Checking", url["url"], "...", end="")

    url["parsed"] = True

    # Get content
    try:
        r = requests.get(url["url"])
    except requests.exceptions.InvalidURL:
        url["error"] = "Invalid URL"
        print("")
        return
    except requests.exceptions.ConnectionError:
        url["error"] = "Connection error"
        print("")
        return
    except requests.exceptions.MissingSchema:
        url["error"] = "Missing schema"
        print("")
        return

    url["code"] = r.status_code
    print(r.status_code)

    # If non-200, log error and bail
    if r.status_code != 200:
        return

    url_parts = urlparse(url["url"])

    # Parse page for content
    if url_parts.netloc == start_url_parts.netloc:
        parser.feed(r.text)


def run():
    url = next_url()

    while url:
        handle_url(url)
        url = next_url()

    print("")
    print("All done!")
    print(urls)


start_url = args.url
start_url_parts = urlparse(start_url)
base_url = start_url_parts.scheme + "://" + start_url_parts.netloc

add_url(start_url)
run()
