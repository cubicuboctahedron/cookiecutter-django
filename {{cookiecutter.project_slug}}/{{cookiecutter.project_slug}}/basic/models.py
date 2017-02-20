from __future__ import unicode_literals

from django.db import models
from django import forms

from wagtail.wagtailcore import fields
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel, FieldPanel, \
    InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailforms.models import AbstractForm
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
{% if cookiecutter.use_translations == 'y' %}from wagtail_modeltranslation.models import TranslationMixin{% endif %}
from wagtail.wagtailcore.blocks import TextBlock, StructBlock, StreamBlock, \
    FieldBlock, CharBlock, RichTextBlock, RawHTMLBlock
from modelcluster.fields import ParentalKey


class PullQuoteBlock(StructBlock):
    quote = TextBlock("quote title")
    attribution = CharBlock()

    class Meta:
        icon = "openquote"


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(
        choices=(
            ('left',
             'Wrap left'),
            ('right',
             'Wrap right'),
            ('mid',
             'Mid width'),
            ('full',
             'Full width'),
        ))


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('normal', 'Normal'), ('full', 'Full width'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()

    class Meta:
        icon = "code"


class BasicStreamBlock(StreamBlock):
    h2 = CharBlock(icon="title", classname="title")
    h3 = CharBlock(icon="title", classname="title")
    h4 = CharBlock(icon="title", classname="title")
    intro = RichTextBlock(icon="pilcrow")
    paragraph = RichTextBlock(icon="pilcrow")
    aligned_image = ImageBlock(label="Aligned image", icon="image")
    pullquote = PullQuoteBlock()
    aligned_html = AlignedHTMLBlock(icon="code", label='Raw HTML')
    document = DocumentChooserBlock(icon="doc-full-inverse")


class Image(models.Model):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]

    class Meta:
        abstract = True


class ImageGalleryItem(Orderable, Image):
    page = ParentalKey('basic.BasicPage', related_name='gallery')


class AbstractBasicPage({%- if cookiecutter.use_translations == 'y' -%}TranslationMixin, {%- endif -%}Page):

    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = fields.RichTextField(blank=True)
    body = fields.StreamField(BasicStreamBlock(), null=True)

    class Meta:
        abstract = True

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('body'),
        InlinePanel('gallery', label="Images"),
    ]


class AbstractBasicFormPage({%- if cookiecutter.use_translations == 'y' -%}TranslationMixin, {%- endif -%}AbstractForm):

    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = fields.RichTextField(blank=True)
    body = fields.StreamField(BasicStreamBlock(), null=True)
    submit_text = RichTextField(blank=True)

    class Meta:
        abstract = True

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('body'),
        InlinePanel('gallery', label="Images"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('submit_text', classname="full"),
    ]


class BasicPage(AbstractBasicPage):
    pass
