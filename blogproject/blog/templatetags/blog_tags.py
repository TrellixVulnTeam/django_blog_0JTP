from django import template
from ..models import Post,Category,Tag
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag
def get_newest_posts():
    return Post.objects.all()[:3]

@register.simple_tag
def get_recent_posts():
    return Post.objects.all()[:]

@register.simple_tag
def get_category():
    return Category.objects.all()


@register.simple_tag
def archives():
    return Post.objects.dates('modified_time','day',order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post'))


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post'))