from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
{% if cookiecutter.use_translations == 'y' %}from wagtail_modeltranslation.models import TranslationMixin{% endif %}
from modelcluster.fields import ParentalKey
from ..basic.models import AbstractBasicPage, Image


class AboutPageImageGalleryItem(Orderable, Image):
    page = ParentalKey('pages.AboutPage', related_name='gallery')


class AboutPage(AbstractBasicPage):
    pass

class AboutIndexPage({%- if cookiecutter.use_translations == 'y' -%}TranslationMixin, {%- endif -%}Page):

    class Meta:
        verbose_name = 'About Us Items'

    intro = RichTextField(blank=True)

    def get_context(self, request):
        abouts = AboutPage.objects.live()

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(abouts, 10)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        context = super(AboutIndexPage, self).get_context(request)
        context['abouts'] = abouts
        return context

    content_panels = [
        FieldPanel('title', classname="full title"),
    ]
