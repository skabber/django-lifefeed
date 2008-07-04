import re
from django import template
from django.conf import settings
from django.template import loader, Context
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from friendfeed import FriendFeed

register = template.Library()

re_twitter = re.compile(r"(@(.+?\b))") # regex for matching twitter @ names
sub_twitter =  r'<a href="http://twitter.com/\2">\1</a>'
re_link = re.compile(r"(http.*?)(?:\s|$)") # regex for matching http links
sub_link = r'<a href="\1">\1</a> '
netflix_re = r'.*/(\d+)$' # regex for capturing netflix movie id's

try:
    googleMapsKey = settings.GOOGLE_MAPS_KEY
except AttributeError:
    googleMapsKey = ""

DEFAULT_TEMPLATE = "friendfeed.html"

def addExtraData(item):
    """
    adds some extra data to the item json
    """
    if item['service']['id'] == 'netflix':
        item['netflixId'] = re.match(netflix_re, item['link']).groups()[0]

def linkify(value):
    """
    replaces commonly known patterns with links
    """
    value = re.sub(re_link, sub_link, value)
    value = re.sub(re_twitter, sub_twitter, value)
    return mark_safe(force_unicode(smart_str(value)))

def lifefeed(username, n=20):
    stream = FriendFeed().fetch_user_feed(username)
    html = ""
    items = stream["entries"][:n]
    for item in items:
        addExtraData(item)
        t = loader.select_template(("%s.html" % item['service']['id'], DEFAULT_TEMPLATE))
        c = Context({'item': item, 'googleMapsKey': googleMapsKey})
        html += t.render(c)
    return html

register.filter(linkify)
register.simple_tag(lifefeed)
