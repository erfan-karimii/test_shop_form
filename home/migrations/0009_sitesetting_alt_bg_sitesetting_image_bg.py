# Generated by Django 4.0.6 on 2022-08-27 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='alt_bg',
            field=models.CharField(max_length=100, null=True, verbose_name='توضیح عکس بک گراند'),
        ),
        migrations.AddField(
            model_name='sitesetting',
            name='image_bg',
            field=models.ImageField(null=True, upload_to='', verbose_name='عکس بک گراند صفحات داخلی'),
        ),
    ]