# Generated by Django 4.0.6 on 2022-08-29 07:53

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_vizhegi_alter_product_takhfif'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('text', ckeditor.fields.RichTextField()),
            ],
        ),
    ]