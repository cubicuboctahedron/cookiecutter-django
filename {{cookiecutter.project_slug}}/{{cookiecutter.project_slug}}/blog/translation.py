{%- if cookiecutter.use_translations == 'y' -%}
from .models import BlogPost, EventPage, BlogIndexPage, EventIndexPage
from wagtail_modeltranslation.translator import TranslationOptions
from wagtail_modeltranslation.decorators import register


@register(BlogPost)
class BlogPostTranslation(TranslationOptions):
    fields = (
        'intro',
        'body',
    )


@register(EventPage)
class EventPageTranslation(TranslationOptions):
    fields = (
        'intro',
        'location',
        'body',
    )


@register(BlogIndexPage)
class BlogIndexPageTranslation(TranslationOptions):
    fields = (
        'intro',
    )


@register(EventIndexPage)
class EventIndexPageTranslation(TranslationOptions):
    fields = (
        'intro',
    )
{%- endif -%}
