# Generated by Django 3.2.7 on 2021-09-05 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='social_media.comment'),
        ),
    ]