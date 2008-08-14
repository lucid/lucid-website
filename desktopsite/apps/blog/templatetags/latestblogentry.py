from django import template
from desktopsite.apps.blog.models import Entry
import datetime

class LatestBlogEntriesNode(template.Node):
    def __init__(self, num, varname):
        self.num, self.varname = num, varname

    def render(self, context):
        context[self.varname] = list(Entry.objects.filter(pub_date__lte=datetime.datetime.now())[:self.num])
        return ''

def do_get_latest_blog_entries(parser, token):
    """
    {% get_latest_blog_entries 2 as latest_entries %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError, "'%s' tag takes three arguments" % bits[0]
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return LatestBlogEntriesNode(bits[1], bits[3])

register = template.Library()
register.tag('get_latest_blog_entries', do_get_latest_blog_entries)

class BlogArchiveNode(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = list(Entry.objects.filter(pub_date__lte=datetime.datetime.now()).dates("pub_date", "month").distinct())
        return ''

def do_get_blog_archive_list(parser, token):
    """
    {% get_blog_archive_list as dates %}
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "'%s' tag takes two arguments" % bits[0]
    if bits[1] != 'as':
        raise template.TemplateSyntaxError, "First argument to '%s' tag must be 'as'" % bits[0]
    return BlogArchiveNode(bits[2])

register.tag('get_blog_archive_list', do_get_blog_archive_list)