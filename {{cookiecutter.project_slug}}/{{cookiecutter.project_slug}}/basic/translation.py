{%- if cookiecutter.use_translations == 'y' -%}
from .models import BasicPage
from wagtail_modeltranslation.translator import TranslationOptions
from wagtail_modeltranslation.decorators import register


@register(BasicPage)
class BasicPageTranslation(TranslationOptions):
    fields = (
        'intro',
        'body',
    )
{%- endif -%}
