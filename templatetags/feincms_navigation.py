from django import template
from feincms.models import Page
from feincms.templatetags.utils import *

register = template.Library()


class NavigationNode(SimpleAssignmentNodeWithVarAndArgs):
    """
    Example:
    {% feincms_navigation of page as sublevel level=2 %}
    {% for p in sublevel %}
        <a href="{{ p.get_absolute_url }}">{{ p.title }}</a>
    {% endfor %}
    """

    def what(self, instance, args):
        level = int(args.get('level', 1))

        if level <= 1:
            return Page.objects.toplevel_navigation()

        if instance.level+2 == level:
            return instance.children.in_navigation()

        try:
            return instance.get_ancestors()[level-2].children.in_navigation()
        except IndexError:
            return []
register.tag('feincms_navigation', do_simple_assignment_node_with_var_and_args_helper(NavigationNode))



