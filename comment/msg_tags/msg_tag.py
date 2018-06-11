from ..models import Comment,Admire_record
from django import template
register=template.Library()
@register.simple_tag
def get_unread_msg():
    return