# Generated by Django 2.2.6 on 2019-10-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0002_auto_20191027_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='tv',
            name='tv_path',
            field=models.CharField(default='abir', max_length=350),
            preserve_default=False,
        ),
    ]
