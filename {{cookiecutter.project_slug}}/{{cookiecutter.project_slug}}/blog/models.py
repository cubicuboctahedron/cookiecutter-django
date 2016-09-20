from itertools import chain

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailforms.models import AbstractFormField
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, \
    InlinePanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
{% if cookiecutter.use_translations == 'y' %}from wagtail_modeltranslation.models import TranslationMixin{% endif %}
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from ..basic.models import AbstractBasicPage, AbstractBasicFormPage, \
    BasicStreamBlock, Image


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPost', related_name='tagged_items')


class BlogPostImageGalleryItem(Orderable, Image):
    page = ParentalKey('blog.BlogPost', related_name='gallery')


class BlogPost(AbstractBasicPage):

    class Meta:
        verbose_name = 'Blog Post'

    date = models.DateField("Post date")
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    content_panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('intro', classname="full"),
        FieldPanel('date'),
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('body'),
        InlinePanel('gallery', label='Images'),
        FieldPanel('tags'),
    ]


class EventPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.EventPage', related_name='tagged_items')


class EventImageGalleryItem(Orderable, Image):
    page = ParentalKey('blog.EventPage', related_name='gallery')


class EventFormField(AbstractFormField):
    page = ParentalKey('EventPage', related_name='form_fields')


class EventPage(AbstractBasicFormPage):

    class Meta:
        verbose_name = 'Event'

    date = models.DateField("Post date")
    date_from = models.DateField("Start date")
    date_to = models.DateField(
        "End date",
        null=True,
        blank=True,
        help_text="Not required if event is on a single day"
    )
    time_from = models.TimeField("Start time", null=True, blank=True)
    time_to = models.TimeField("End time", null=True, blank=True)
    location = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=EventPageTag, blank=True)

    content_panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('intro', classname="full"),
        FieldPanel('date'),
        FieldPanel('date_from'),
        FieldPanel('date_to'),
        FieldPanel('time_from'),
        FieldPanel('time_to'),
        FieldPanel('location'),
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('body'),
        InlinePanel('gallery', label='Images'),
        FieldPanel('tags'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('submit_text', classname="full"),
    ]


class BlogIndexPage({%- if cookiecutter.use_translations == 'y' -%}TranslationMixin, {%- endif -%}Page):

    class Meta:
        verbose_name = 'Blog Post List'

    intro = RichTextField(blank=True)

    def get_context(self, request):
        posts = BlogPost.objects.live().order_by('-date')

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(posts, 10)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = posts
        return context

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
    ]


class EventIndexPage({%- if cookiecutter.use_translations == 'y' -%}TranslationMixin, {%- endif -%}Page):

    class Meta:
        verbose_name = 'Event List'

    intro = RichTextField(blank=True)

    def get_context(self, request):
        events = EventPage.objects.live().order_by('-date_from')

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(events, 10)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        context = super(EventIndexPage, self).get_context(request)
        context['events'] = events
        return context

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
    ]
