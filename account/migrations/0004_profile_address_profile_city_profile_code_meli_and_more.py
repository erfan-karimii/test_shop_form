# Generated by Django 4.0.6 on 2022-08-31 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_myuser_is_verify'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='code_meli',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='code_posty',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
