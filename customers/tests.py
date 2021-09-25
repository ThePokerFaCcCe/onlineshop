from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from PIL import Image
import tempfile
import os
from .models import Customer


def upload_img_url(user_id):
    return reverse('customers:users-profile-image', args=[user_id])


class PictureModelUploadTest(TestCase):
    def setUp(self):  # Call before any test_... .
        self.client = APIClient()
        self.user = get_user_model().objects.create_user('sagsag', 'sss')
        self.client.force_authenticate(self.user)

    def test_upload_image(self):
        with tempfile.NamedTemporaryFile(suffix='.jpg') as f:
            img = Image.new('RGB', (10, 10))
            img.save(f, format='JPEG')
            f.seek(0)  # Set pointer at first of file
            res = self.client.post(upload_img_url(self.user.pk), {'profile_image': f}, format='multipart')
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK, msg=res.data)
        self.assertIn('profile_image', res.data)
        self.assertNotEqual(self.user.profile_image, res.data['profile_image'])
        self.assertTrue(os.path.exists(self.user.profile_image.image.path))
        self.user.profile_image.image.delete()

    def test_upload_bad_image(self):
        res = self.client.post(upload_img_url(self.user.pk), {'profile_image': 'LOL im fake'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=res.data)
