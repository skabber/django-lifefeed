import re
from django import template
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from friendfeed import FriendFeed

register = template.Library()

re_twitter = re.compile(r"(@(.+?\b))")
sub_twitter =  r'<a href="http://twitter.com/\2">\1</a>'
re_link = re.compile(r"(http.*?)(?:\s|$)")
sub_link = r'<a href="\1">\1</a> '

def linkify(value):
    value = re.sub(re_link, sub_link, value)
    value = re.sub(re_twitter, sub_twitter, value)
    return mark_safe(force_unicode(smart_str(value)))

def lifefeed(username):
    stream = FriendFeed().fetch_user_feed(username)
    items = stream["entries"]
    return render_to_string("friendfeed.html", {"items": items})

register.filter(linkify)
register.simple_tag(lifefeed)
