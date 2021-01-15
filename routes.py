# Flask Webapp
from flask import Flask, redirect, url_for
from jinja2 import Template

from storageservice import sample_random_lands

app = Flask(__name__)
template = Template(open("index.html").read())

@app.route("/")
def landranker():
    """
    Homepage of Landranker Site.
    Offer user ability to select land from random sample
    """
    return "Hello World"
#    land1, land2 = sample_random_lands()
#    webpage = template.render(A=land1["s3_url"], B=land2["s3_url"])
#    return webpage

@app.after_request
def add_header(response):
    response.headers["Pragma"] = "no-cache"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = "0"
    return response
