import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def sync_default_site(sender, **kwargs):
    if sender.label != 'sites':
        return

    domain = os.getenv('SITE_DOMAIN') or os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if not domain:
        domain = next(
            (
                host
                for host in settings.ALLOWED_HOSTS
                if host not in {'127.0.0.1', 'localhost'}
            ),
            '127.0.0.1',
        )

    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            'domain': domain,
            'name': os.getenv('SITE_NAME', 'Leadly'),
        },
    )