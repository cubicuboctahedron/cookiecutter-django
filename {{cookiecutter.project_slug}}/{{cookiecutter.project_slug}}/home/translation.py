from .models import HomePage
from wagtail_modeltranslation.translator import TranslationOptions
from wagtail_modeltranslation.decorators import register


@register(HomePage)
class HomePageTranslation(TranslationOptions):
    fields = (
        'intro',
        'body',
    )
