# Generated by Django 2.1 on 2018-11-07 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0033_auto_20181106_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]