
from django import template
from posts.models import Post
register = template.Library()
from django.middleware import csrf
import re
@register.filter(name='one_more')
def one_more(_1, _2):
    return _1, _2

# def search_tag(tag, request):
#     token_url = request.path + '?'+str(request.META.get('CSRF_COOKIE', None))
#     current_url = request.get_full_path()
#     search_query = request.GET.get('search_query')
#     # search_tag = request.GET.get('search_tag')
#     print(search_tag,search_query)
#     if search_query:
#         return token_url + '&?search_query='+str(search_query) +'&?search_tag='+str(tag)
#     else:
#         return token_url +'&?search_tag='+str(tag)
# register.filter(search_tag)
# dictonary
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# select correct color for label
@register.filter
def qual(rate):
    return 'gray' if rate == 0 else 'orange' if rate <=3 else 'yell' if rate <= 6 else 'blue' if rate <= 8 else 'green'

@register.filter()
def to_int(value):
    return int(value)

@register.filter()
def order_title(value):
    if value == 'rate_asc':
        return 'Low Rated First'
    elif value == 'date_asc':
        return 'Oldest First'
    elif value == 'rate_desc':
        return 'High Rated First'
    else:
        return 'Newest First'

import html
@register.filter()
def html_decode(s):
    return html.unescape(s)

@register.simple_tag
def get_bootstrap_alert_msg_css_name(tags):
    return "danger" if tags == "error" else tags

@register.filter()
def count_tag(tagname):
    count = Post.objects.filter(tags=tagname).count()
    return count
