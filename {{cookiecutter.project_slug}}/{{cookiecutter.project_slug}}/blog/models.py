from itertools import chain

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailcore.fields import StreamField, RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, \
    InlinePanel, PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail_modeltranslation.models import TranslationMixin
from wagtail.wagtailsearch import index
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from ..basic.models import BasicStreamBlock, Image


class Entry(TranslationMixin, Page):

    class Meta:
        abstract = True

    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BasicStreamBlock())
    date = models.DateField("Post date")

    search_fields = Page.search_fields + (
        index.SearchField('body'),
    )

    content_panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('date'),
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('body'),
        InlinePanel('gallery', label='Images'),
        FieldPanel('tags'),
    ]


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPost', related_name='tagged_items')


class BlogPostImageGalleryItem(Orderable, Image):
    page = ParentalKey('blog.BlogPost', related_name='gallery')


class BlogPost(Entry):
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    class Meta:
        verbose_name = 'Blog Post'


class EventPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.EventPage', related_name='tagged_items')


class EventImageGalleryItem(Orderable, Image):
    page = ParentalKey('blog.EventPage', related_name='gallery')


class EventPage(Entry):

    class Meta:
        verbose_name = 'Event'

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

    search_fields = Entry.search_fields + (
        index.SearchField('location'),
    )

    content_panels = [
        FieldPanel('title', classname='full title'),
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
    ]


class BlogIndexPage(TranslationMixin, Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + (
        index.SearchField('intro'),
    )

    def get_context(self, request):
        news = BlogPost.objects.live().order_by('-date')
        events = EventPage.objects.live().order_by('-date')

        pages = sorted(chain(news, events), key=lambda instance: instance.date,
                       reverse=True)

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(pages, 10)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        context = super(BlogIndexPage, self).get_context(request)
        context['entries'] = entries
        return context

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('intro', classname="full"),
    ]
