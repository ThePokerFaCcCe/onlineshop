from rest_framework.settings import api_settings
from rest_framework.fields import ImageField


class PictureField(ImageField):
    def _make_url(self, value):
        try:
            url = value.url
        except AttributeError:
            return None
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    def _make_data(self, value):
        if not value:
            return None
        return {
            'url': self._make_url(value),
            'name': value.name,
        }

    def to_representation(self, value):
        if not value:
            return None
        # use_url = getattr(self, 'use_url', api_settings.UPLOADED_FILES_USE_URL)
        return {
            'image': self._make_data(value.image),
            'thumbnail': self._make_data(value.thumbnail),
        }
