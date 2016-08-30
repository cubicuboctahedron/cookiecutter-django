from .models import BlogPost, EventPage, BlogIndexPage
from wagtail_modeltranslation.translator import TranslationOptions
from wagtail_modeltranslation.decorators import register


@register(BlogPost)
class BlogPostTranslation(TranslationOptions):
    fields = (
        'body',
    )


@register(EventPage)
class EventPageTranslation(TranslationOptions):
    fields = (
        'location',
        'body',
    )


@register(BlogIndexPage)
class BlogIndexPageTranslation(TranslationOptions):
    fields = (
        'intro',
    )
