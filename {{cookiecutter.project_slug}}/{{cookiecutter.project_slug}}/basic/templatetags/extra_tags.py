from itertools import chain

from django import template

from ..models import Page

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('basic/elements/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None, css_class="navbar-default"):
    menuitems = Page.objects.live().in_menu()
    for menuitem in menuitems:
        # we don't directly check if calling_page is none since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.url == menuitem.url
                           if calling_page else False)
    return {
        'css_class': css_class,
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }
