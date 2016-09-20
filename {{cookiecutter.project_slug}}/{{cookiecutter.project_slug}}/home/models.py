from wagtail.wagtailcore.models import Orderable

from wagtail_modeltranslation.models import TranslationMixin
from modelcluster.fields import ParentalKey

from ..basic.models import AbstractBasicPage, Image


class HomePageImageGalleryItem(Orderable, Image):
    page = ParentalKey('home.HomePage', related_name='gallery')


class HomePage(AbstractBasicPage):
    pass
