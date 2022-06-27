AUTHOR = "Redowan Delowar"
SITENAME = "Redowan's Reflections"
SITEURL = ""
PORT = 5000

PATH = "content"

TIMEZONE = "Asia/Dhaka"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "https://getpelican.com/"),
    ("Python.org", "https://www.python.org/"),
    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
    ("You can modify those links in your config file", "#"),
)

# Social widget
SOCIAL = (
    ("https://twitter.com/rednafi", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 1
THEME = "elegant"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.admonition": {},
    },
}

# Tell pelican where your custom.css file is in your content folder.
STATIC_PATHS = ["extras/custom.css"]

# Tell pelican where it should copy that file to in your output folder
EXTRA_PATH_METADATA = {"extras/custom.css": {"path": "theme/css/custom.css"}}

# Tell the pelican-bootstrap-3 theme where to find the custom.css file in your output folder
CUSTOM_CSS = "theme/css/custom.css"

# Elegant theme specific
RECENT_ARTICLES_COUNT = 11
SITE_DESCRIPTION = """
        Ruminations on software.
        Python, Django, Microservices, PostgreSQL,
        Redis, AWS, Go, Open Source.
"""

LANDING_PAGE_TITLE = ""
SITE_LICENSE = """© 2020-2022 • Redowan Delowar • All Rights Reserved"""


# SEO
CLAIM_GOOGLE = "<meta name='google-site-verification' content='N5QEPRj-LpgoEY0Hf3uVMmZq8kjDwTFjd54IgvLmRBc' />"

FEATURED_IMAGE = "https://user-images.githubusercontent.com/30027932/149235389-c6b85b40-5515-4de4-a922-7b0f91efd0cf.png"

SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "daily", "indexes": "daily", "pages": "daily"},
}
