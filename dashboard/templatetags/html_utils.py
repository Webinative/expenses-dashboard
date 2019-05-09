from django import template
register = template.Library()


@register.filter
def html_linebreaks(text):
    """replaces new lines \n with html linebreaks <br>
    """

    return text.replace('\n', '<br>')
