# Generated by Django 2.2.6 on 2019-10-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tv',
            name='backdrop',
            field=models.ImageField(blank=True, upload_to='media/tv/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='tv',
            name='poster',
            field=models.ImageField(blank=True, upload_to='media/tv/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='tv',
            name='tmdb_title',
            field=models.CharField(blank=True, max_length=350),
        ),
    ]