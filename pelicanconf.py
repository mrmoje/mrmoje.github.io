# -*- coding: utf-8 -*-
from __future__ import unicode_literals

AUTHOR = u"James Nzomo"
SITENAME = u"TDT"
SITEURL = u"http://tdt.rocks"
SITE_SUBTEXT = "Thoughts & Deeds on Tech"
TIMEZONE = u"Africa/Nairobi"

# can be useful in development, but set to False when you're ready to publish
RELATIVE_URLS = True

GITHUB_URL = "http://github.com/mrmoje/mrmoje.github.io"
DISQUS_SITENAME = "tdtrocks"
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True
LOCALE = "C"
DEFAULT_PAGINATION = 4
DEFAULT_DATE = (1969, 12, 31, 23, 59, 59)
DELETE_OUTPUT_DIRECTORY = True

# Feeds
FEED_ATOM = 'feed/atom.xml'
FEED_DOMAIN = SITEURL

# LINKS = (("kili", "http://kili.io"),)

SOCIAL = (("github", "https://github.com/mrmoje"),
          ("twitter", "https://twitter.com/mrmoje"),
          ("rss", "http://tdt.rocks/feed/atom.xml"),
          ("stackoverflow", "https://stackoverflow.com/users/1002644/moje"))

# global metadata to all the contents
# DEFAULT_METADATA = (('key', 'val'),)

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
}

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'img',
    'js',
    'css',
    'extra/robots.txt',
    'CNAME',
    'README.md',
    'BingSiteAuth.xml',
]

# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

MD_EXTENSIONS = [
    'toc',
    'codehilite',
    'attr_list'
]

PLUGIN_PATHS = [
    './pelican-plugins'
]

PLUGINS=[
    'sitemap'
]

# tdt specific prefs
THEME = "pelican-alchemy/alchemy"
HIDE_SIDEBAR = True
CUSTOM_CSS = 'css/overrides.css'
SHOW_ARTICLE_AUTHOR = True
PAGES_ON_MENU = True
CATEGORIES_ON_MENU = True
TAGS_ON_MENU = False
ARCHIVES_ON_MENU = False
DEFAULT_DATE_FORMAT = ('%B %d, %Y')
