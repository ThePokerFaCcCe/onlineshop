"""
I think this is a very bad way to do that but it works :))
"""

import os
from typing import Any, Optional, Tuple
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile, ImageFileDescriptor
from PIL import Image
from io import BytesIO
import os
from datetime import datetime
from django.conf import settings

SEPARATE_STR = '*'


class PictureFileField:
    def __init__(self, image, thumbnail):
        self.image = image
        self.thumbnail = thumbnail


class PictureDescriptor(ImageFileDescriptor):
    def _create_file(self, instance, field, path):
        return ImageFieldFile(instance, field, path)

    def __get__(self, instance, cls=None):
        data = super().__get__(instance, cls)
        if isinstance(data, ImageFieldFile):
            text = data.name
            if SEPARATE_STR not in text:
                return data

            img, thumb = text.split(SEPARATE_STR, 1)
            return PictureFileField(
                image=self._create_file(instance, data.field, img),
                thumbnail=self._create_file(instance, data.field, thumb)
            )

        return data


class PictureField(ImageField):
    """
    Custom ImageField with thumbnail support

    ---    
    usage
    -----
    when `make_thumbnail = True`:
    >>> field.image
    < ImageFieldFile ...>
    >>> field.thumbnail
    < ImageFieldFile ...>
    
    """
    descriptor_class = PictureDescriptor
    
    def _upload_to_path(self,instance, filename,*args,**kwargs):
        now = datetime.now()
        return "{model_name}/{year}/{month}/{day}/{hour}-{minute}-{microsecond}{extension}".format(
            
            model_name = instance.__class__.__name__,
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            microsecond=now.microsecond,
            extension=os.path.splitext(filename)[1],
        )

    def __init__(self, upload_to='',use_upload_to_func:bool=False, make_thumbnail: bool = False,
                 verbose_name: Optional[str] = None, name: Optional[str] = None,
                 width_field: Optional[str] = None, height_field: Optional[str] = None,
                 thumbnail_size: Tuple[int, int] = (200, 200),
                 **kwargs: Any
                 ) -> None:
        """
        Parameters
        -----------
        use_upload_to_func : bool
            A function that creates path for files.
            {model_name}/{year}/{month}/{day}/{hour}-{minute}-{microsecond}{extension}
        """
        self.thumbnail_size, self.make_thumbnail = thumbnail_size, make_thumbnail
        if use_upload_to_func:
            upload_to = self._upload_to_path
        super().__init__(upload_to=upload_to, verbose_name=verbose_name, name=name, width_field=width_field, height_field=height_field, **kwargs)

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)
        if self.make_thumbnail:
            thumb_path = self._make_thumbnail(file)
            file.name = SEPARATE_STR.join([file.name, thumb_path])
            setattr(model_instance, self.attname, file)
        return file

    def _make_thumbnail(self, image):
        img_relpath = os.path.relpath(image.path, settings.BASE_DIR)
        img_dir, img_name = os.path.split(img_relpath)

        thumb_name = f"thumb_{img_name}"
        thumb_path = os.path.join(img_dir, thumb_name)

        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(self.thumbnail_size)
        img.save(thumb_path)

        img_relpath_no_media_root = os.path.relpath(
            image.path, settings.__dict__.get('MEDIA_ROOT', '.')
        )

        img_dir_no_media_root = os.path.split(
            img_relpath_no_media_root
        )[0]

        thumb_path_no_media_root = os.path.join(
            img_dir_no_media_root, thumb_name
        )

        return thumb_path_no_media_root

    def get_prep_value(self, value: Any) -> Any:
        # print('[PRE] - ', value)
        return super().get_prep_value(value)
