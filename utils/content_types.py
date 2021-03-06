from django.contrib.contenttypes.models import ContentType
from django.db.utils import ProgrammingError

from products.models import Product

PRODUCT = None

try:
    ContentType.objects.get_for_model(Product)

except ProgrammingError:
    print("WARNING: We couldn't get ContentType model in database, if you are trying to migrate, don't care about this message")

else:
    PRODUCT = ContentType.objects.get_for_model(Product)
