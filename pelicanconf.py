#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Max Richter"
SITENAME = "Deep Blue - Data, Tech & Engineering"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/Berlin"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "http://getpelican.com/"),
    ("Python.org", "http://python.org/"),
    ("Jinja2", "http://jinja.pocoo.org/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "./attila/"

# To set background image for the home page.
# HOME_COVER = "https://casper.ghost.org/v1.0.0/images/welcome.jpg"
HOME_COVER = "images/post-bg.jpg"

# Analytics
# GOOGLE_ANALYTICS = "UA-3546274-12"

AUTHORS_BIO = {
    "maxrichter": {
        "name": "Max Richter",
        "cover": "images/spacex.jpg",
        "image": "images/avatar_new.png",
        "website": "https://maxrichter.github.io/",
        "linkedin": "max-richter-59b62b134/",
        "github": "MaxRichter",
        "location": "Germany",
        "bio": "Data, data everywhere! Software Engineering Manager with interest in Data Engineering and Science.",
    }
}
