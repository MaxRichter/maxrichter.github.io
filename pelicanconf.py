#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Max Richter"
SITENAME = "Deep Blue - Data, Tech & Leadership"
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

STATIC_PATHS = ["assets"]

EXTRA_PATH_METADATA = {
    "assets/robots.txt": {"path": "robots.txt"},
    "assets/favicon.ico": {"path": "favicon.ico"},
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "./attila/"

# To set background image for the home page.
# HOME_COVER = "https://casper.ghost.org/v1.0.0/images/welcome.jpg"
HOME_COVER = "assets/images/home_cover.jpg"

AUTHORS_BIO = {
    "maxrichter": {
        "name": "Max Richter",
        "cover": "assets/images/home_cover.jpg",
        "image": "assets/images/avatar.png",
        "website": "https://maxrichter.github.io/",
        "linkedin": "max-richter-59b62b134/",
        "github": "MaxRichter",
        "location": "Germany",
        "bio": "Data, data everywhere! Software Engineering Manager with interest in Data- Engineering, Science and Leadership.",
    }
}
