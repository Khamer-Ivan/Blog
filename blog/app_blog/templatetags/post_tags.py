from django import template

from app_blog.models import Post

register = template.Library()


@register.simple_tag()
def all_post_list(**kwargs):
    return Post.objects.filter(profile=kwargs['pk'])