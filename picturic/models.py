from .fields import PictureField
from django.db.models import Model

class PictureModel(Model):
    pic=PictureField(make_thumbnail=True,use_upload_to_func=True)
