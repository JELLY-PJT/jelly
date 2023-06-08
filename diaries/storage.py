import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CustomStorage(FileSystemStorage):

    location = os.path.join(settings.MEDIA_ROOT, "uploads/images/")
    base_url = urljoin(settings.MEDIA_URL, "uploads/images/")