# Generated by Django 2.1 on 2018-12-13 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0047_auto_20181213_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(),
        ),
    ]