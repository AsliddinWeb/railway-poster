# Generated by Django 5.0 on 2023-12-15 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_alter_maxsulot_options_cartitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='qoshimcha_matn',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='qoshimcha_rasm',
            field=models.ImageField(blank=True, null=True, upload_to='qoshimcha-rasmlar'),
        ),
    ]
