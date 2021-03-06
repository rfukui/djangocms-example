from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage


class StaticRootS3BotoStorage(S3BotoStorage):

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'static'
        super(StaticRootS3BotoStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        url = super(StaticRootS3BotoStorage, self).url(name)
        if url.endswith('admin'):
            url += '/'
        return url


class MediaRootS3BotoStorage(S3BotoStorage):

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        super(MediaRootS3BotoStorage, self).__init__(*args, **kwargs)


class CachedS3BotoStorage(StaticRootS3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
