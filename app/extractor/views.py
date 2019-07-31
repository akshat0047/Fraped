from flask import Flask, render_template, request, flash, Blueprint, url_for, jsonify
from app.extractor.forms import ApiForm
from scrapy.crawler import CrawlerRunner
from spiders import HeadersSpider
import glob
import requests


# Get file paths of all modules.
modules = glob.glob('subdirectory/*.py')

# Create some test data for our catalog in the form of a list of dictionaries.
#extract = Blueprint('extract', __name__, url_prefix='/extract')

crawl_runner = CrawlerRunner()      # requires the Twisted reactor to run
data_list = []                    # store quotes
scrape_in_progress = False
scrape_complete = False


def crawl_for_spiders(spidy, url, depth):
    """
    Scrape for quotes
    """
    global scrape_in_progress
    global scrape_complete

    if not scrape_in_progress:
        scrape_in_progress = True
        global data_list
        # start the crawler and execute a callback when complete
        eventual = crawl_runner.crawl(
            spidy, url=url, depth=depth, data_list=data_list)
        eventual.addCallback(finished_scrape)
    #    return 'SCRAPING'
    # elif scrape_complete:
    #    return 'SCRAPE COMPLETE'
    # return 'SCRAPE IN PROGRESS'


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True
    if scrape_complete:
        return json.dumps(data_list)


@app.route('/', methods=['GET', 'POST'])
def home():

    form = ApiForm(request.form)
    if request.method == 'POST':
        print("true")
        link = request.form['url']
        print(link)
        choice = request.form['Extract']
        depth = request.for['Depth']
        print(choice)
        if choice == 'sp':
            return crawl_for_spiders("headers", link, depth)
        if choice == 'dh':
            return crawl_for_spiders("headersd", link, depth)
        if choice == 'lop':
            return crawl_for_spiders("urls", link, depth)
        if choice == 'lopd':
            return crawl_for_spiders("urlsd", link, depth)

    elif request.method == 'GET':
        print("here")
        return render_template('extractor/index.html', form=form)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods=['GET', 'POST'])
def api_view():
    html = "<h2>Welcome to API</h2>" + "<ul>" + "<li>Links On a Page '/api/v1/links?url=your_url'</li>" + "<li>Links On a Page '/api/v1/links?url=your_url'</li>" + "<li>Links On a Domain '/api/v1/domain_links?url=your_url'</li>" + \
        "<li>Headers On a Page '/api/v1/page?url=your_url'</li>" + "<li>Headers on First Children '/api/v1/first_children_headers?url=your_url'</li>" + \
        "<li>Headers on First Children '/api/v1/domain_headers?url=your_url'</li>"

    return html
