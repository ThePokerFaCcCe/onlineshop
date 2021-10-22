from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField, DateTimeField, PositiveIntegerField, TextField, BooleanField
from django.db.models.fields.related import ForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

User = settings.AUTH_USER_MODEL




class Tag(Model):
    label = CharField(max_length=50)

class TaggedItem(Model):
    tag = ForeignKey(to=Tag,on_delete=CASCADE)

    content_type = ForeignKey(to=ContentType,on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()




class Like(Model):
    user = ForeignKey(to=User,on_delete=CASCADE)

    content_type = ForeignKey(to=ContentType,on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()


class Comment(MPTTModel):
    text = TextField(max_length=300)
    hidden = BooleanField(default=False,blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    user = ForeignKey(to=User,on_delete=CASCADE)
    reply_to = TreeForeignKey(to='self', on_delete=CASCADE, related_name="reply",null=True,blank=True)

    content_type = ForeignKey(to=ContentType,on_delete=CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()

    class MPTTMeta:
        order_insertion_by = ['created_at']
        parent_attr = 'reply_to'
