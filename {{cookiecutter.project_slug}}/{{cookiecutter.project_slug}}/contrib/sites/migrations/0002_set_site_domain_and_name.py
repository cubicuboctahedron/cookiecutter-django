"""
To understand why this file is here, please read:

http://cookiecutter-django.readthedocs.io/en/latest/faq.html#why-is-there-a-django-contrib-sites-directory-in-cookiecutter-django
"""
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def update_site_forward(apps, schema_editor):
    """Set site domain and name."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': '{{cookiecutter.domain_name}}',
            'name': '{{cookiecutter.project_name}}'
        }
    )
    Site.objects.update_or_create(
        id=2,
        defaults={
            'domain': '{{cookiecutter.project_name}}.dev',
            'name': '{{cookiecutter.project_name}}'
        }
    )


def update_site_backward(apps, schema_editor):
    """Revert site domain and name to default."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'example.com',
            'name': 'example.com'
        }
    )
    Site.objects.filter(id=2).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
