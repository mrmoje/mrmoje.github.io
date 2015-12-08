# -*- coding: utf-8 -*-
from __future__ import unicode_literals

AUTHOR = u"James Nzomo"
SITENAME = u"TDT"
SITEURL = ""
SITE_SUBTEXT = "Thoughts & Deeds on Tech"
TIMEZONE = u"Africa/Nairobi"

# can be useful in development, but set to False when you're ready to publish
RELATIVE_URLS = True

GITHUB_URL = "http://github.com/mrmoje/mrmoje.github.io"
# DISQUS_SITENAME = ""
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True
LOCALE = "C"
DEFAULT_PAGINATION = 4
DEFAULT_DATE = (1969, 12, 31, 23, 59, 59)

FEED_ALL_RSS = "feeds/all.rss.xml"
CATEGORY_FEED_RSS = "feeds/%s.rss.xml"

# LINKS = (("kili", "http://kili.io"),)

SOCIAL = (("github", "https://github.com/mrmoje"),
          ("twitter", "https://twitter.com/mrmoje"),
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
    'CNAME'
]

# code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

# tdt specific prefs
THEME = "pelican-alchemy/alchemy"
HIDE_SIDEBAR = True
CUSTOM_CSS = 'css/overrides.css'
SHOW_ARTICLE_AUTHOR = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_ARCHIVES_ON_MENU = False
DEFAULT_DATE_FORMAT = ('%B %d, %Y')
