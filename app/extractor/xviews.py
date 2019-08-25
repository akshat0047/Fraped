
from flask import Flask, render_template, request, flash, Blueprint, url_for, jsonify,redirect
from app.extractor.forms import ApiForm
from scrapy.crawler import CrawlerRunner
from app.extractor.spiders.headers import HeadersSpider
from app.extractor.spiders.headersd import HeadersDSpider
from app.extractor.spiders.urls import UrlsSpider
from app.extractor.spiders.urlsd import UrlsDSpider
from flask_cors import CORS
import requests, json, os, time, crochet, subprocess

# Create some test data for our catalog in the form of a list of dictionaries.
#extract = Blueprint('extract', __name__, url_prefix='/extract')

crawl_runner = CrawlerRunner()      # requires the Twisted reactor to run
data_list = []                    # store quotes
scrape_in_progress = False
scrape_complete = False

extractor = Blueprint('extract', __name__, url_prefix='/extract')
CORS(extractor)


def crawl_for_spiders(spidy, url, data_list, depth=0):
    """
    Scrape for quotes
    """
    print("Requested Spiders")
    eventual = crawl_runner.crawl(spidy, meta={"url": url, "depth": depth}, data_list=data_list)
    eventual.addCallback(finished_scrape)
           
@extractor.route('/results', methods=['POST','GET'])
def get_results():
    """
    Get the results only if a spider has results
    """
    global scrape_in_progress
    global scrape_complete
    if scrape_complete:
        return {"res": "finished"}
    return {"scrape in progress":scrape_in_progress}


@extractor.route('/show_results', methods=['POST','GET'])
def show_results():
    """
    Get the results only if a spider has results
    """
    global scrape_in_progress
    global scrape_complete
    global data_list
    if scrape_complete:
        return {"Scraped": data_list}
    return {'Incomplete List':data_list}


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """

    global scrape_complete
    scrape_complete = True
    print("Flag Set")



@extractor.route('/', methods=['POST','GET'])
def home():
    global scrape_in_progress
    global scrape_complete
    global data_list
    data_list = []
    scrape_in_progress = False
    scrape_complete = False

    form = ApiForm(request.form)
    if request.method == 'POST':
        print("true")
        link = request.form['url']
        print(link)
        choice = request.form['Extract']
        print(choice)
        if choice == 'sp':
          
             if not scrape_in_progress:
               scrape_in_progress = True
               print("Crawling..")
               crawl_for_spiders(HeadersSpider, link, data_list)
               while not scrape_complete:
                  print("Waiting... %s" % scrape_complete)
                  time.sleep(0.10)
               return {'statusajax': 'scraping','scrape progress':scrape_in_progress}
             elif scrape_complete:
               return {'statusajax': 'scrape complete'}
             return {'statusajax': 'scrape in progress'}
             """
             subprocess.check_output(['scrapy', 'crawl', 'headers', "-o", "output.json"])
             with open("output.json") as items_file:
             return items_file.read()
             """
        if choice == 'dh':
            depth = request.form['Depth']
            if not scrape_in_progress:
               scrape_in_progress = True
               # start the crawler and execute a callback when complete
               crawl_for_spiders(HeadersDSpider, link, data_list, depth)
              # while not scrape_complete: time.sleep(0.1)
               return {'statusajax': 'scraping','scrape progress':scrape_in_progress}
            elif scrape_complete:
               return {'statusajax': 'scrape complete'}
            return {'statusajax': 'scrape in progress'}

        if choice == 'lop':
            if not scrape_in_progress:
               scrape_in_progress = True
               # start the crawler and execute a callback when complete
               crawl_for_spiders(UrlsSpider, link, data_list)
               while not scrape_complete: time.sleep(0.1)
               return {'statusajax': 'scraping','scrape progress':scrape_in_progress}
            elif scrape_complete:
               return {'statusajax': 'scrape complete'}
            return {'statusajax': 'scrape in progress'}

        if choice == 'lopd':
            depth = request.form['Depth']
            if not scrape_in_progress:
               scrape_in_progress = True
               # start the crawler and execute a callback when complete
               crawl_for_spiders(UrlsDSpider, link, data_list, depth)
               while not scrape_complete: time.sleep(0.1)
               return {'statusajax': 'scraping','scrape progress':scrape_in_progress}
            elif scrape_complete:
               return {'statusajax': 'scrape complete'}
            return {'statusajax': 'scrape in progress'}


    elif request.method == 'GET':
        print("here")
        return render_template('extractor/index.html', form=form)

"""
#@extractor.after_request
#def add_header(r):
 
#   Add headers to both force latest IE rendering engine or Chrome Frame,
#    and also to cache the rendered page for 10 minutes.
    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
"""
