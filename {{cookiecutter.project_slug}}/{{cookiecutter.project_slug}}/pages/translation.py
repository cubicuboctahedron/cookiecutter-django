from .models import AboutPage, AboutIndexPage
from wagtail_modeltranslation.translator import TranslationOptions
from wagtail_modeltranslation.decorators import register


@register(AboutPage)
class AboutPageTranslation(TranslationOptions):
    fields = (
        'intro',
        'body',
    )

@register(AboutIndexPage)
class AboutIndexPageTranslation(TranslationOptions):
    fields = (
        'intro',
    )
