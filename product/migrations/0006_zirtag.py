# Generated by Django 4.1 on 2022-08-25 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_size_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZirTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sargroh', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.tag')),
            ],
        ),
    ]
