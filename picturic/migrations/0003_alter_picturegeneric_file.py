# Generated by Django 3.2.7 on 2021-10-03 15:23

from django.db import migrations
import picturic.fields
import picturic.utils


class Migration(migrations.Migration):

    dependencies = [
        ('picturic', '0002_auto_20210929_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picturegeneric',
            name='file',
            field=picturic.fields.PictureField(max_length=9999, upload_to=picturic.utils.upload_to_path_generic),
        ),
    ]
