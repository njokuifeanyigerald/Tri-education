# Generated by Django 3.0.4 on 2020-03-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0006_postview'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='PostView',
        ),
    ]
