from django.db.models import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import PositiveIntegerField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .utils import upload_to_path_generic
from .fields import PictureField


class PictureGeneric(Model):
    file = PictureField(make_thumbnail=True, upload_to=upload_to_path_generic)

    content_type = ForeignKey(to=ContentType, on_delete=CASCADE, related_name="pictures")
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()
